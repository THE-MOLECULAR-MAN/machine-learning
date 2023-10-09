#!/bin/bash
# Tim H 2023

# UNFINISHED

# https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-delete-domain.html

# remove existing versions (old v1) of AWS CLI:
brew uninstall awscli
pip uninstall awscli
python3.10 -m pip uninstall awscli

cd ~/Downloads || exit 1
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
installer -pkg AWSCLIV2.pkg \
    -target CurrentUserHomeDirectory \
    -applyChoiceChangesXML awscli2-installconfig.xml

# list directories in  PATH where I can write to it
# MUST be in bash, not zsh for this to work:
PATH_LIST=$(echo "$PATH")
for iter_path in ${PATH_LIST//:/ }
do
    if [[ -d "$iter_path" ]]; then
        ls -dlah "$iter_path" # | grep "$(whoami)"
    fi
done

WRITEABLE_PATH="/opt/homebrew/bin"
INSTALL_PATH="/Users/thonker/aws-cli"

# create symlinks for 
ln -s "$INSTALL_PATH/aws" "$WRITEABLE_PATH/aws"
ln -s "$INSTALL_PATH/aws_completer" "$WRITEABLE_PATH/aws_completer"

# test install, version, and symlinks:
which aws
aws --version

# show the config and creds files, if they exist
cat ~/.aws/config ~/.aws/credentials

# test AWS connection, creds:
aws sts get-caller-identity
aws iam get-user
aws s3 ls

# https://jmespath.org/
# list the apps running - verified working
ARRAY_APPS=$(aws sagemaker list-apps --output text \
    --query "Apps[?Status=='InService'].AppName,AppType,UserProfileName")

for iter_appid in ${ARRAY_APPS}
do
    echo "going to delete $iter_appid"
done

# needs to be moved inside the loop and additional vars need to be grabbed.
aws sagemaker delete-app \
    --domain-id "$SAGEMAKER_DOMAIN_ID" \
    --app-name AppName \
    --app-type AppType \
    --user-profile-name UserProfileName

    