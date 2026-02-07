#!/usr/bin/env python3
"""
并行Subagent执行引擎

功能：
1. 解析v2 JSON计划（包含subtasks和aggregation配置）
2. 为每个task的subtasks生成并行Task调用
3. 收集和聚合JSON结果
4. 跟踪性能指标，验证优化效果

使用方法：
python parallel_executor.py nvidia-dcf-valuation-plan-v2-parallel.json
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class ParallelExecutor:
    """并行Subagent执行引擎"""

    def __init__(self, plan_path: str):
        self.plan_path = Path(plan_path)
        self.plan = self._load_plan()
        self.execution_log = []
        self.start_time = None

    def _load_plan(self) -> Dict[str, Any]:
        """加载并验证JSON计划"""
        with open(self.plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)

        # 验证v2格式
        if not plan.get('version', '').startswith('2.'):
            raise ValueError(f"需要v2格式计划，当前版本: {plan.get('version')}")

        return plan

    def _build_wave_structure(self) -> List[List[int]]:
        """根据依赖关系构建波次执行结构"""
        tasks = {t['id']: t for t in self.plan['tasks']}
        waves = []
        completed = set()

        while len(completed) < len(tasks):
            # 找出所有依赖已满足的任务
            ready = []
            for task_id, task in tasks.items():
                if task_id not in completed:
                    deps = task.get('dependencies', [])
                    if all(d in completed for d in deps):
                        ready.append(task_id)

            if not ready:
                raise ValueError("检测到循环依赖")

            waves.append(ready)
            completed.update(ready)

        return waves

    def _generate_subtask_prompt(self, task: Dict, subtask: Dict) -> str:
        """为subtask生成Agent提示词"""
        topic = self.plan['topic']

        prompt = f"""你是金融研究专家，正在执行以下研究任务的一个子任务：

# 研究主题
{topic}

# 主任务
{task['description']}

# 你的子任务
{subtask['description']}

# 数据查询要求
"""

        if 'data_queries' in subtask:
            prompt += "请使用MCP工具查询以下数据：\n"
            for i, query in enumerate(subtask['data_queries'], 1):
                prompt += f"{i}. {query}\n"
        elif 'task' in subtask:
            prompt += f"{subtask['task']}\n"

        # 输出格式要求
        output_format = subtask.get('output_format', 'json')
        if output_format == 'json':
            prompt += """
# 输出格式
请以JSON格式返回结果，包含：
```json
{
  "subtask_id": "子任务ID",
  "data": {
    // 查询到的数据，结构化组织
  },
  "summary": "数据摘要（1-2句话）"
}
```
"""
        else:
            prompt += f"\n# 输出格式\n{output_format}\n"

        return prompt

    def _generate_aggregation_prompt(self, task: Dict, subtask_results: List[Dict]) -> str:
        """为aggregation生成提示词"""
        topic = self.plan['topic']
        agg_config = task['aggregation']

        prompt = f"""你是金融研究专家，正在整合子任务的分析结果。

# 研究主题
{topic}

# 主任务
{task['description']}

# 子任务结果
以下是{len(subtask_results)}个并行子任务的结果：

"""

        for i, result in enumerate(subtask_results, 1):
            prompt += f"## 子任务{i}: {result.get('subtask_id', f'subtask-{i}')}\n"
            prompt += f"```json\n{json.dumps(result.get('data', {}), indent=2, ensure_ascii=False)}\n```\n\n"

        prompt += f"""
# 你的任务
{agg_config['description']}

# 输出要求
- 字数：约{agg_config.get('estimated_time', '90秒')}对应的内容量
- 结构：清晰的章节和要点
- 数据：引用具体数字和趋势
- 分析：提供洞察和结论
"""

        return prompt

    def execute_task_with_parallel_subagents(self, task: Dict) -> Tuple[str, float]:
        """执行单个task，使用并行subagent模式"""
        task_id = task['id']
        task_desc = task['description']

        print(f"\n{'='*60}")
        print(f"Task {task_id}: {task_desc}")
        print(f"{'='*60}")

        task_start = time.time()

        # 检查是否使用并行subagent策略
        if task.get('execution_strategy') != 'parallel_subagents':
            print(f"⚠️  Task {task_id} 不使用并行subagent策略，跳过")
            return None, 0

        subtasks = task.get('subtasks', [])
        if not subtasks:
            print(f"⚠️  Task {task_id} 没有定义subtasks，跳过")
            return None, 0

        print(f"\n📋 将并行执行 {len(subtasks)} 个子任务:")
        for st in subtasks:
            print(f"  - {st['id']}: {st['description']}")

        # 生成并行Task调用指令
        print(f"\n🚀 生成并行Task调用配置...")

        parallel_calls = []
        for subtask in subtasks:
            prompt = self._generate_subtask_prompt(task, subtask)
            model = subtask.get('model', 'haiku')

            call_config = {
                'subtask_id': subtask['id'],
                'description': subtask['description'],
                'model': model,
                'prompt': prompt,
                'estimated_time': subtask.get('estimated_time', '未知')
            }
            parallel_calls.append(call_config)

        # 显示调用配置
        print(f"\n📝 并行调用配置:")
        for i, call in enumerate(parallel_calls, 1):
            print(f"  {i}. Subtask {call['subtask_id']}: {call['description']}")
            print(f"     Model: {call['model']}, Est: {call['estimated_time']}")

        # ⚠️ 注意：在实际Claude Code环境中，这里应该使用Task tool并行调用
        # 示例XML结构（在Claude Code中实际执行）：
        # <function_calls>
        #   <invoke name="Task">
        #     <parameter name="subagent_type">general-purpose</parameter>
        #     <parameter name="description">子任务1描述</parameter>
        #     <parameter name="model">haiku</parameter>
        #     <parameter name="prompt">...</parameter>
        #   </invoke>
        #   <invoke name="Task">
        #     <parameter name="subagent_type">general-purpose</parameter>
        #     <parameter name="description">子任务2描述</parameter>
        #     <parameter name="model">haiku</parameter>
        #     <parameter name="prompt">...</parameter>
        #   </invoke>
        #   ...
        # </function_calls>

        print(f"\n⏳ 模拟并行执行（实际环境中将使用Task tool）...")

        # 模拟结果（实际应从Task tool获取）
        subtask_results = []
        for call in parallel_calls:
            result = {
                'subtask_id': call['subtask_id'],
                'data': {'模拟数据': f"这是{call['subtask_id']}的模拟结果"},
                'summary': f"{call['description']}完成"
            }
            subtask_results.append(result)

        subtask_duration = time.time() - task_start
        print(f"✅ {len(subtask_results)}个子任务完成，耗时: {subtask_duration:.1f}秒")

        # Aggregation阶段
        agg_start = time.time()
        agg_config = task.get('aggregation', {})

        if agg_config:
            print(f"\n🔄 聚合阶段: {agg_config['description']}")
            agg_prompt = self._generate_aggregation_prompt(task, subtask_results)
            agg_model = agg_config.get('model', 'sonnet')

            print(f"   Model: {agg_model}")
            print(f"   预计耗时: {agg_config.get('estimated_time', '未知')}")

            # 模拟aggregation执行
            print(f"   ⏳ 模拟聚合执行...")
            time.sleep(1)  # 模拟

            agg_duration = time.time() - agg_start
            print(f"   ✅ 聚合完成，耗时: {agg_duration:.1f}秒")

        total_duration = time.time() - task_start

        # 记录执行日志
        log_entry = {
            'task_id': task_id,
            'description': task_desc,
            'subtasks_count': len(subtasks),
            'subtask_duration': subtask_duration,
            'aggregation_duration': agg_duration if agg_config else 0,
            'total_duration': total_duration,
            'estimated_time': task.get('total_estimated_time', '未知')
        }
        self.execution_log.append(log_entry)

        print(f"\n✅ Task {task_id} 完成:")
        print(f"   子任务并行执行: {subtask_duration:.1f}秒")
        if agg_config:
            print(f"   聚合: {agg_duration:.1f}秒")
        print(f"   总计: {total_duration:.1f}秒")
        print(f"   预计: {task.get('total_estimated_time', '未知')}")

        return f"Task {task_id} 输出（模拟）", total_duration

    def execute(self) -> Dict[str, Any]:
        """执行完整的研究计划"""
        print(f"\n{'='*70}")
        print(f"🚀 开始执行并行Subagent优化计划")
        print(f"{'='*70}")
        print(f"计划: {self.plan_path.name}")
        print(f"主题: {self.plan['topic']}")
        print(f"版本: {self.plan.get('version', 'unknown')}")
        print(f"优化策略: {self.plan.get('optimization', {}).get('strategy', 'unknown')}")
        print(f"预期提速: {self.plan.get('optimization', {}).get('expected_speedup', 'unknown')}")

        self.start_time = time.time()

        # 构建波次结构
        waves = self._build_wave_structure()
        print(f"\n📊 执行计划: {len(waves)}个波次")

        wave_results = []

        for wave_idx, task_ids in enumerate(waves, 1):
            print(f"\n{'='*70}")
            print(f"Wave {wave_idx}: 并行执行 {len(task_ids)} 个任务")
            print(f"{'='*70}")

            wave_start = time.time()
            tasks = [t for t in self.plan['tasks'] if t['id'] in task_ids]

            # 在实际环境中，这里应该并行执行所有任务
            # 对于task-level并行，仍然使用原有的Task tool
            # 对于subtask-level并行，使用上面的parallel_subagents模式

            wave_task_results = []
            for task in tasks:
                result, duration = self.execute_task_with_parallel_subagents(task)
                wave_task_results.append({
                    'task_id': task['id'],
                    'result': result,
                    'duration': duration
                })

            wave_duration = time.time() - wave_start
            wave_results.append({
                'wave': wave_idx,
                'tasks': task_ids,
                'duration': wave_duration
            })

            print(f"\n✅ Wave {wave_idx} 完成，耗时: {wave_duration:.1f}秒")

        total_duration = time.time() - self.start_time

        # 生成执行报告
        report = self._generate_report(wave_results, total_duration)

        return report

    def _generate_report(self, wave_results: List[Dict], total_duration: float) -> Dict[str, Any]:
        """生成执行报告"""
        print(f"\n{'='*70}")
        print(f"📊 执行报告")
        print(f"{'='*70}")

        baseline_time = 28.3 * 60  # 28.3分钟转秒
        predicted_time = float(self.plan.get('optimization', {}).get('expected_time', '10分钟').split('分')[0]) * 60

        print(f"\n⏱️  时间统计:")
        print(f"   实际执行时间: {total_duration:.1f}秒 ({total_duration/60:.1f}分钟)")
        print(f"   基线时间: {baseline_time:.1f}秒 (28.3分钟)")
        print(f"   预测时间: {predicted_time:.1f}秒 ({predicted_time/60:.1f}分钟)")

        if baseline_time > 0:
            speedup = ((baseline_time - total_duration) / baseline_time) * 100
            print(f"   提速: {speedup:.1f}%")

        print(f"\n📋 波次详情:")
        for wave_result in wave_results:
            print(f"   Wave {wave_result['wave']}: {wave_result['duration']:.1f}秒 (Tasks: {wave_result['tasks']})")

        print(f"\n📋 任务详情:")
        for log in self.execution_log:
            print(f"   Task {log['task_id']}: {log['total_duration']:.1f}秒")
            print(f"      - 子任务: {log['subtasks_count']}个, {log['subtask_duration']:.1f}秒")
            if log['aggregation_duration'] > 0:
                print(f"      - 聚合: {log['aggregation_duration']:.1f}秒")
            print(f"      - 预计: {log['estimated_time']}")

        report = {
            'plan_file': str(self.plan_path),
            'plan_version': self.plan.get('version'),
            'execution_time': {
                'total_seconds': total_duration,
                'total_minutes': total_duration / 60,
                'baseline_seconds': baseline_time,
                'predicted_seconds': predicted_time,
                'speedup_percent': ((baseline_time - total_duration) / baseline_time) * 100 if baseline_time > 0 else 0
            },
            'waves': wave_results,
            'tasks': self.execution_log,
            'timestamp': datetime.now().isoformat()
        }

        # 保存报告
        report_path = self.plan_path.parent / f"execution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n💾 报告已保存: {report_path}")

        return report


def main():
    if len(sys.argv) < 2:
        print("使用方法: python parallel_executor.py <plan.json>")
        sys.exit(1)

    plan_path = sys.argv[1]

    if not Path(plan_path).exists():
        print(f"错误: 文件不存在: {plan_path}")
        sys.exit(1)

    executor = ParallelExecutor(plan_path)
    report = executor.execute()

    print(f"\n{'='*70}")
    print(f"✅ 执行完成")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
