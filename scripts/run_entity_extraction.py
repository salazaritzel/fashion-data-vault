# this is the runner
# 1. Load articles from database (last 30/60/90 days)
# 2. Extract seasons (EntityRuler)
# 3. Extract brands (EntityRuler + default NER)
# 4. Extract materials (EntityRuler)
# 5. Extract trends (Matcher - your 5 patterns)
# 6. Save results (either update articles table or create summary table)

# Output: Either:

# Option A: Update aggregates_trend with extracted keywords column
# Option B: Create a new trend_summary table with counts