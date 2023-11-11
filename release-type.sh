#!/bin/bash

# Assign command line arguments to variables
github_event_type=$1
github_ref=$2

# Function to echo the output in a format that's easy to parse in Python
output_result() {
    echo "variants=${variants}"
    echo "type=${type}"
}

# Default values
variants="[]"
type="develop"

# Determining build type based on provided arguments
if [ "$github_event_type" = "pull_request" ]; then
    variants="[]"
    type="develop"
elif [[ "$github_ref" == refs/tags/ot3* ]]; then
    variants='["internal-release"]'
    type="release"
elif [[ "$github_ref" == refs/tags/v* ]]; then
    variants='["release"]'
    type="release"
elif [[ "$github_ref" == refs/heads/internal-release* ]]; then
    variants='["internal-release"]'
    type="develop"
elif [[ "$github_ref" == refs/heads/release* ]] || [[ "$github_ref" == refs/heads/chore_release* ]]; then
    variants='["release"]'
    type="develop"
elif [ "$github_ref" = "refs/heads/edge" ]; then
    variants='["release", "internal-release"]'
    type="develop"
elif [[ "$github_ref" == *app-build-internal ]]; then
    variants='["internal-release"]'
    type="develop"
elif [[ "$github_ref" == *app-build ]]; then
    variants='["release"]'
    type="develop"
elif [[ "$github_ref" == *app-build-both ]]; then
    variants='["release", "internal-release"]'
    type="develop"
else
    variants="[]"
    type="develop"
fi

# Output the result
output_result
