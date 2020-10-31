# install packages to a temporary directory and zip it
pip3 install -r requirements.txt --target ./packages

cd packages
zip -9mrv packages.zip .
mv packages.zip ..
cd ..

# remove temporary directory and requirements.txt
rm -rf packages