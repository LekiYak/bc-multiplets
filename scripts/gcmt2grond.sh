#!/bin/bash

# Assign arguments (expecting positional arguments)
read -r _ mrr mtt mpp mrt mrp mtp exponent <<< "$@"

# Adjust exponent
adj_exp=$((exponent - 7))

# Perform mappings and sign changes
mnn_fmt=$(awk "BEGIN {printf \"%.3fe+%d\", $mtt, $adj_exp}")
mee_fmt=$(awk "BEGIN {printf \"%.3fe+%d\", $mpp, $adj_exp}")
mdd_fmt=$(awk "BEGIN {printf \"%.3fe+%d\", $mrr, $adj_exp}")
mne_fmt=$(awk "BEGIN {printf \"%.3fe+%d\", -1 * $mtp, $adj_exp}")
mnd_fmt=$(awk "BEGIN {printf \"%.3fe+%d\", $mrt, $adj_exp}")
med_fmt=$(awk "BEGIN {printf \"%.3fe+%d\", -1 * $mrp, $adj_exp}")

# Output in required format
echo "mnn = $mnn_fmt"
echo "mee = $mee_fmt"
echo "mdd = $mdd_fmt"
echo "mne = $mne_fmt"
echo "mnd = $mnd_fmt"
echo "med = $med_fmt"
