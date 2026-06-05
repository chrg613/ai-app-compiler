# Quick Fix Reference

## What Was Broken
The turn-by-turn chat had 5 critical bugs preventing it from working:

| Bug | Error | Impact |
|-----|-------|--------|
| Dictionary Access | `'dict' object has no attribute 'intent'` | All endpoints failed when trying to access compilation result |
| Refine Logic | No recompilation on changes | Mid-conversation refinement didn't work |
| Flask Collisions | `AssertionError: View function mapping is overwriting endpoint` | App regeneration crashed |
| Generate App | `AttributeError` on dict access | Download ZIP failed |
| UI Update | Changes not reflected visually | Users didn't see updated assumptions |

## What Was Fixed

### 1. main.py - Lines 299-324
**Change:** `result.intent` → `result['intent']`  
**Why:** `compiler_pipeline.compile()` returns a dict, not an object

### 2. main.py - Lines 357-472
**Change:** Complete rewrite of `refine_requirements()`  
**Why:** Now actually recompiles with accumulated user messages and shows updated assumptions

### 3. src/codegen/flask_generator.py - Lines 180-188
**Change:** Removed `/app-health` endpoint from generated code  
**Why:** Framework already provides these routes; removed collision

### 4. main.py - Lines 475-523
**Change:** Safe dict extraction in `generate_app()`  
**Why:** Fixed type mismatch when reading stored result

### 5. static/js/app.js - Lines 254-290
**Change:** Show assumptions after refinement  
**Why:** Now displays updated structure and assumptions from refined compilation

## Testing the Fix

Start the app and try this flow:

```
1. User: "Build a task manager with tasks and users"
   → System: Shows assumptions (2 entities, 2 roles)
   
2. User clicks "Change Something"
   
3. User: "Add projects to group tasks"
   → System: Recompiles, shows 3 entities now, updates preview
   
4. Click "Download App"
   → ZIP downloads successfully with all changes included
```

## Key Behavior Changes

✅ **Assumptions shown with confidence scores** (0.6-0.9)  
✅ **Clarification questions are context-aware**  
✅ **Refinement actually recompiles the app**  
✅ **Updated structure shown in preview after changes**  
✅ **No more Flask endpoint collisions**  
✅ **ZIP download works with refined requirements**  

## Files to Update Directly

If applying manually:

1. **main.py**
   - Search for `result.intent` (lines ~300)
   - Replace with `result['intent']`
   - Rewrite entire `refine_requirements()` function (lines 357-472)
   - Fix `generate_app()` dict access (lines 475-523)

2. **src/codegen/flask_generator.py**
   - Find `_generate_main()` function (line 181)
   - Remove the `/app-health` route generation lines

3. **static/js/app.js**
   - Find `applyChanges()` method (line 254)
   - Add assumption display and preview update after refinement

## Verification Checklist

Run through this to confirm fixes work:

- [ ] Start conversation - no `'dict' object has no attribute 'intent'` error
- [ ] Send requirement - assumptions displayed correctly
- [ ] Click modify - modal appears without error
- [ ] Submit change - new assumptions shown (not old ones)
- [ ] Download app - ZIP created successfully
- [ ] Check ZIP - includes updated conversation history

## If Something Still Breaks

Check these first:

1. **"dict has no attribute X" error** → Check you're using `result['key']` not `result.key`
2. **Endpoint collision error** → Verify `/app-health` route is removed from generator
3. **Refine shows old assumptions** → Confirm full refine endpoint rewrite (all 116 lines)
4. **Download fails** → Check generate-app dict extraction code
5. **UI doesn't update** → Verify `this.showAssumptions(data.response)` call in applyChanges()
