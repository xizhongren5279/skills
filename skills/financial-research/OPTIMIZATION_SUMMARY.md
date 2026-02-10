# Financial Research Skill Optimization Summary

## Executive Summary

The original SKILL.md failed to enforce critical workflow steps, leading to models skipping:
1. Reading reference documents
2. Creating JSON plans
3. Using Task tool for parallel execution
4. Saving to output directory

The optimized version applies **discipline-enforcing patterns** from writing-skills to prevent these violations.

---

## Key Changes

### 1. Fixed CSO (Claude Search Optimization)

**BEFORE** (578 chars):
```yaml
description: Comprehensive financial research skill for company research, industry analysis, strategy research, macro research, and quantitative analysis. Use when users request any type of financial research tasks, investment analysis, market analysis, economic research, or data-driven financial insights. Supports queries like "研究XX行业的竞争格局", "分析XX宏观经济指标", "对比XX和XX公司", "制定XX投资策略", or any financial research needs beyond simple one-page company reports.
```

**AFTER** (242 chars):
```yaml
description: Use when users request financial research beyond simple one-page summaries - company deep-dives, industry analysis, strategy research, macro research, or quantitative analysis requiring structured investigation with data retrieval and synthesis
```

**Why Better**:
- ✅ Starts with "Use when..." (triggering condition first)
- ✅ Under 500 characters (better token efficiency)
- ✅ NO workflow summary (prevents Claude skipping full skill)
- ✅ Focuses on WHEN not WHAT

---

### 2. Added "The Iron Law" Section

**NEW - Front and Center**:
```markdown
## The Iron Law

NO DIRECT MCP QUERIES WITHOUT A JSON PLAN FIRST
NO ANALYSIS WITHOUT TASK TOOL EXECUTION
NO COMPLETION WITHOUT OUTPUT FILES SAVED
```

**Purpose**: Makes non-negotiable requirements unmissable

---

### 3. Added Comprehensive Red Flags Section

**NEW - Catches Rationalizations Early**:
```markdown
## Red Flags - STOP and Follow Process

| Thought | Reality |
|---------|---------|
| "I'll just query MCP directly" | Plan first. No exceptions. |
| "The plan is obvious, I'll skip JSON" | Write the JSON. Plans expose assumptions. |
| "I can execute queries myself faster" | Use Task tool. Parallelism matters. |
| "I'll save files at the end" | Create output dir now. Prevents forgetting. |
...
```

**Impact**: Model can self-check before violating workflow

---

### 4. Added "Spirit vs Letter" Declaration

**NEW - At Top**:
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

**Purpose**: Cuts off entire class of "I'm following the spirit" rationalizations

---

### 5. Enhanced Step 2 Enforcement

**BEFORE**:
```markdown
### Step 2: Read Reference Documents

**MANDATORY**: Before creating any plan, read the relevant reference documents:
```

**AFTER**:
```markdown
### Step 2: Read Reference Documents

**MANDATORY - NO EXCEPTIONS**: Before Step 3, you MUST read these files using Read tool:

[List of files]

**DO NOT**:
- ❌ Skip reading because "I know MCP tools"
- ❌ Skim and proceed
- ❌ Read while planning (read BEFORE planning)
- ❌ Rely on memory from previous sessions

**Red Flags for Step 2 Violations**:
- You're writing JSON plan without having read references
- You're making MCP queries without reading mcp_tools.md
- You think you already know the content

| Excuse | Reality |
|--------|---------|
| "I used MCP tools before" | Syntax changes. Parameters vary. Read it. |
...
```

**Additions**:
- ✅ "NO EXCEPTIONS" emphasis
- ✅ Explicit DO NOT list
- ✅ Red flags for self-checking
- ✅ Rationalization table

---

### 6. Enhanced Step 3 (JSON Plan) Enforcement

**BEFORE**:
```markdown
### Step 3: Create Research Plan

Based on the request and reference documents, create a structured research plan:

**Plan Structure**:
```

**AFTER**:
```markdown
### Step 3: Create Research Plan

**REQUIRED OUTPUT**: Valid JSON plan structure (see below)

**MANDATORY REQUIREMENTS**:
1. MUST generate complete JSON plan
2. MUST save plan to `{output_dir}/plan.json`
3. MUST validate structure before Step 4
4. MUST show plan to user before execution

[JSON structure]

**DO NOT**:
- ❌ Skip JSON and do narrative description
- ❌ Make plan "in your head" without writing it
- ❌ Start execution without user seeing plan
- ❌ Proceed with invalid JSON structure

**Red Flags for Step 3 Violations**:
- Moving to queries without JSON file created
- Thinking "plan is simple, I'll skip formalism"
- Starting to explain what you'll do instead of writing JSON

| Excuse | Reality |
|--------|---------|
| "Plan is obvious" | Writing exposes assumptions and gaps. |
...
```

**Additions**:
- ✅ "MUST" 4x in requirements
- ✅ Explicit DO NOT list
- ✅ Red flags section
- ✅ Rationalization table
- ✅ Save plan.json as part of Step 3

---

### 7. Enhanced Step 4 (Task Tool) Enforcement

**BEFORE**:
```markdown
### Step 4: Execute Research Plan

Once the JSON plan is generated:

[Descriptive text about what happens]

For each wave:
- Spawn ALL tasks in the wave using Task tool...
```

**AFTER**:
```markdown
### Step 4: Execute Research Plan

**MANDATORY TOOL**: Use `Task` tool with `subagent_type="general-purpose"`

**REQUIRED EXECUTION PATTERN**:
1. Parse plan into execution waves
2. For EACH wave, spawn ALL tasks in parallel using Task tool in ONE message
3. Wait for wave completion before proceeding to next wave
4. Collect task outputs

**DO NOT**:
- ❌ Execute MCP queries yourself
- ❌ Run tasks sequentially when they can be parallel
- ❌ Skip Task tool and do inline execution
- ❌ Forget to pass task context to subagents

**Red Flags for Step 4 Violations**:
- Calling mcp__ashare-mcp-research tools directly in main conversation
- Running tasks one at a time when they have no dependencies
- Thinking "Task tool overhead isn't worth it"

| Excuse | Reality |
|--------|---------|
| "I'm faster than Task tool" | You're sequential. Task tool is parallel. |
...
```

**Additions**:
- ✅ "MANDATORY TOOL" header
- ✅ Command language ("MUST", not "should")
- ✅ Explicit DO NOT list
- ✅ Red flags section
- ✅ Rationalization table
- ✅ Specific tool call example

---

### 8. Enhanced Step 6 (File Save) Enforcement

**BEFORE**:
```markdown
**Save output**:
- All files saved to: `output/{topic}_{timestamp}/`
- Confirm with message: "研究报告已保存至: output/{topic}_{timestamp}/"
```

**AFTER**:
```markdown
### Step 6: Save All Output Files

**MANDATORY FILE SAVES**:

output/{topic}_{timestamp}/
├── report.md           ← REQUIRED
├── plan.json           ← REQUIRED
├── retrieval_metadata.json  ← REQUIRED
└── generation_log.md   ← REQUIRED

**CRITICAL**: ALL 4 files must be saved. Missing any file = incomplete execution.

**DO NOT**:
- ❌ Output report to chat only
- ❌ Skip saving metadata
- ❌ Forget generation log
- ❌ Save some files but not all

**Red Flags for Step 6 Violations**:
- Presenting report in chat without file saves
- Thinking "user can see output already"
- Forgetting to create files until user asks

| Excuse | Reality |
|--------|---------|
| "User can see output in chat" | Files enable reproducibility and audit. |
...
```

**Additions**:
- ✅ Visual file tree with "REQUIRED" labels
- ✅ "CRITICAL" emphasis
- ✅ Explicit DO NOT list
- ✅ Red flags section
- ✅ Rationalization table

---

### 9. Added Step 1 Output Dir Creation

**NEW - Prevents Forgetting Step 6**:
```markdown
### Step 1: Understand the Request

**REQUIRED ACTIONS**:
...
4. **Create output directory NOW**:
   ```python
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   output_dir = f"output/{topic}_{timestamp}"
   os.makedirs(output_dir, exist_ok=True)
   ```

**Why create dir now**: Prevents forgetting Step 5. Directory exists = commitment to save files.
```

**Rationale**: Creating dir at start creates psychological commitment to save files at end

---

### 10. Added Comprehensive Rationalization Table

**NEW - Consolidated Anti-Pattern List**:
```markdown
## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "User wants quick answer" | Skill triggered = full process required |
| "This is simple research" | Simple becomes complex. Follow process. |
| "I'll optimize by skipping steps" | Process IS the optimization |
| "Planning wastes time" | Wrong execution wastes MORE time |
| "I know what to do" | Writing plan exposes blind spots |
| "Task tool adds overhead" | Parallelism saves MORE time |
| "I'll save files later" | You'll forget. Save as you go. |
| "Spirit over letter" | Letter IS spirit. No shortcuts. |
```

**Purpose**: Comprehensive lookup table for all common violations

---

### 11. Simplified Structure

**REMOVED**:
- Verbose "Critical Reference Documents" section (moved to Step 2)
- Redundant "Important Guidelines" section (merged into steps)
- Long "Performance Optimization" section (simplified to expectations)
- Detailed field definitions (kept in Step 3 but compressed)

**Token Savings**: ~2000 words → ~1200 words (40% reduction while adding enforcement)

---

## Before/After Comparison

### Description Field
| Aspect | Before | After |
|--------|--------|-------|
| Length | 578 chars | 242 chars |
| Starts with "Use when" | ❌ | ✅ |
| Workflow summary | ❌ (has examples) | ✅ (none) |
| Token efficient | ❌ | ✅ |

### Step 2 Enforcement
| Aspect | Before | After |
|--------|--------|-------|
| "MANDATORY" keyword | ✅ | ✅ |
| DO NOT list | ❌ | ✅ |
| Red flags | ❌ | ✅ |
| Rationalization table | ❌ | ✅ |

### Step 3 Enforcement
| Aspect | Before | After |
|--------|--------|-------|
| "MUST" language | ❌ | ✅ (4x) |
| DO NOT list | ❌ | ✅ |
| Red flags | ❌ | ✅ |
| Rationalization table | ❌ | ✅ |
| Save plan.json | ⚠️ (Step 5) | ✅ (Step 3) |

### Step 4 Enforcement
| Aspect | Before | After |
|--------|--------|-------|
| "MANDATORY" keyword | ❌ | ✅ |
| DO NOT list | ❌ | ✅ |
| Red flags | ❌ | ✅ |
| Rationalization table | ❌ | ✅ |
| Prohibit direct MCP | ⚠️ (implied) | ✅ (explicit) |

### Step 6 Enforcement
| Aspect | Before | After |
|--------|--------|-------|
| File list visibility | ⚠️ (prose) | ✅ (visual tree) |
| "REQUIRED" labels | ❌ | ✅ |
| DO NOT list | ❌ | ✅ |
| Red flags | ❌ | ✅ |
| Rationalization table | ❌ | ✅ |

---

## Expected Behavior Improvements

### Without Optimizations (Observed)
1. ❌ Model skips Step 2 (reading references)
2. ❌ Model skips Step 3 (JSON plan generation)
3. ❌ Model executes MCP queries directly (skips Task tool)
4. ❌ Model outputs to chat only (forgets file saves)
5. ❌ User has to remind model about output directory

### With Optimizations (Expected)
1. ✅ Model reads references before planning
2. ✅ Model creates and saves JSON plan
3. ✅ Model uses Task tool for parallel execution
4. ✅ Model creates output directory in Step 1
5. ✅ Model saves all 4 required files automatically
6. ✅ Model self-checks using red flags sections
7. ✅ Model resists rationalizations via tables

---

## Testing Recommendations

### Pressure Scenarios to Test

**Scenario 1: Time Pressure**
```
User: "快速研究一下宁德时代，我10分钟后要开会"
Expected: Model still follows all 6 steps
Test: Does model skip JSON plan or Task tool?
```

**Scenario 2: Simplicity Rationalization**
```
User: "简单分析一下比亚迪的市场份额"
Expected: Model creates full research workflow
Test: Does model think "too simple for full process"?
```

**Scenario 3: Sunk Cost (mid-execution)**
```
Setup: Model has already executed 3 MCP queries directly
Intervention: "Wait, did you create a JSON plan first?"
Expected: Model stops, admits violation, starts over
Test: Does model rationalize "I'll create plan retroactively"?
```

**Scenario 4: Output Forgetting**
```
Setup: Model completes analysis and presents in chat
Intervention: "Where are the output files?"
Expected: Model immediately saves all 4 files
Test: Did model forget or did model think optional?
```

### Meta-Testing

After each test:
1. Document exact rationalizations model used
2. Check if rationalization table covers it
3. If new rationalization, add to table
4. Re-test to verify plug worked

### Success Criteria

- [ ] 100% compliance with Step 2 (read references)
- [ ] 100% compliance with Step 3 (JSON plan)
- [ ] 100% compliance with Step 4 (Task tool)
- [ ] 100% compliance with Step 6 (file saves)
- [ ] 0 rationalizations not covered by tables
- [ ] Model self-corrects when hitting red flags

---

## Implementation Checklist

- [x] Optimize description field (CSO)
- [x] Add "Iron Law" section
- [x] Add comprehensive red flags section
- [x] Add "spirit vs letter" declaration
- [x] Add Step 2 enforcement (DO NOT, red flags, rationalization)
- [x] Add Step 3 enforcement (DO NOT, red flags, rationalization)
- [x] Add Step 4 enforcement (DO NOT, red flags, rationalization)
- [x] Add Step 6 enforcement (DO NOT, red flags, rationalization)
- [x] Move output dir creation to Step 1
- [x] Add master rationalization table
- [x] Simplify structure (remove redundancy)
- [ ] Test with pressure scenarios
- [ ] Iterate based on observed violations
- [ ] Deploy optimized version

---

## File Diff Summary

**Lines Changed**: 567 lines
**Key Sections Added**: 8
- Iron Law
- Red Flags (master)
- Rationalization Table (master)
- Per-step DO NOT lists (4x)
- Per-step Red Flags (4x)
- Per-step Rationalization Tables (4x)

**Key Sections Modified**: 6
- Description (frontmatter)
- Overview
- All 6 Steps

**Key Sections Removed**: 3
- Verbose "Critical Reference Documents"
- Redundant "Important Guidelines"
- Detailed "Performance Optimization"

**Net Result**: More enforcement, less verbosity

---

## Next Steps

1. **Review optimized SKILL.md**: Read SKILL_OPTIMIZED.md
2. **Run pressure tests**: Use scenarios above
3. **Iterate**: Add rationalizations as discovered
4. **Deploy**: Replace SKILL.md with optimized version
5. **Monitor**: Track compliance in production usage

---

*Optimization completed using writing-skills discipline-enforcing patterns*
