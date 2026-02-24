#!/bin/bash

# Assign arguments (expecting positional arguments)
read -r mnn mee mdd mne mnd med exponent <<< "$@"

# Adjust exponent
adj_exp=$((exponent + 7))

# Perform mappings and sign changes
mtt_fmt=$(awk "BEGIN {printf \"%.3f\", $mnn}")
mpp_fmt=$(awk "BEGIN {printf \"%.3f\", $mee}")
mrr_fmt=$(awk "BEGIN {printf \"%.3f\", $mdd}")
mtp_fmt=$(awk "BEGIN {printf \"%.3f\", -1 * $mne}")
mrt_fmt=$(awk "BEGIN {printf \"%.3f\", $mnd}")
mrp_fmt=$(awk "BEGIN {printf \"%.3f\", -1 * $med}")

# Output in required format
echo "$mrr_fmt $mtt_fmt $mpp_fmt $mrt_fmt $mrp_fmt $mtp_fmt $exponent"
