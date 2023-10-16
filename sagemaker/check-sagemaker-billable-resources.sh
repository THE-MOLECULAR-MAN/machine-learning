#!/bin/bash
# Tim H 2023

# checking billable resources in AWS SageMaker

# --query is CLIENT side filtering of the HTTP response
# https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html
#     --query 'Volumes[*].Attachments[?State==`attached`].VolumeId'
# --filter is SERVER side filtering

set -e

echo "Endpoints:"
aws sagemaker list-endpoints

echo "Compilation Jobs:"
aws sagemaker list-compilation-jobs

echo "Inference experiments:"
aws sagemaker list-inference-experiments

echo "Notebook instances:"
aws sagemaker list-notebook-instances

echo "Processing jobs:"
aws sagemaker list-processing-jobs --query \
    "ProcessingJobSummaries[?ProcessingJobStatus=='InProgress']"

echo "Training jobs:"
aws sagemaker list-training-jobs   --query \
    "TrainingJobSummaries[?TrainingJobStatus=='InProgress']"

echo "Transform Jobs:"
aws sagemaker list-transform-jobs  --query \
    "TransformJobSummaries[?TransformJobStatus=='InProgress']"

echo "Auto ML Jobs:"
aws sagemaker list-auto-ml-jobs    --query \
    "AutoMLJobSummaries[?AutoMLJobStatus=='InProgress']"

echo "Pipelines executing:"
aws sagemaker list-pipeline-executions --pipeline-name comedy-bang-bang-p-sj5f7fkuowj8 --query "PipelineExecutionSummaries[?PipelineExecutionStatus=='Executing']"

echo "Apps:"
aws sagemaker list-apps --query "Apps[?Status=='InService']"

echo "Domains:"
aws sagemaker list-domains


# needs more info:
# echo "Training jobs for hyper-parameter tuning jobs:"
# aws sagemaker list-pipeline-executions
# aws sagemaker list-training-jobs-for-hyper-parameter-tuning-job --hyper-parameter-tuning-job-name 

echo "check-sagemaker-billable-resources.sh finished successfully"

# Don't have status fields:
# aws sagemaker list-experiments
# aws sagemaker list-actions
# aws sagemaker list-pipelines

aws sagemaker list-studio-lifecycle-configs


# aws sagemaker list-trials
