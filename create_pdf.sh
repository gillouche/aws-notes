#!/usr/bin/env bash

build_dir="./build"
mkdir -p output

if ! [ -f "${build_dir}/archi.md" ] || ! [ -f "${build_dir}/big_data.md" ] || ! [ -f "${build_dir}/complete.md" ] || ! [ -f "${build_dir}/devops.md" ] || ! [ -f "${build_dir}/ML.md" ]; then
  echo "Missing files, execute generate_index.py first."
  exit 1
fi

echo "Copying all images from services directory"
find ./services -type f -name "*.png" -exec cp {} ${build_dir} \;
find ./services -type f -name "*.jpg" -exec cp {} ${build_dir} \;
find ./services -type f -name "*.jpeg" -exec cp {} ${build_dir} \;

echo "Copy pandoc config"
cp pygments.theme ${build_dir}
cp inline_code.tex ${build_dir}

cd ${build_dir} || exit

echo "Create archi.pdf"
pandoc -V geometry:a4paper -V geometry:margin=2cm --highlight-style pygments.theme --include-in-header inline_code.tex -o ../output/archi.pdf archi.md --pdf-engine=xelatex

echo "Create big_data.pdf"
pandoc -V geometry:a4paper -V geometry:margin=2cm --highlight-style pygments.theme --include-in-header inline_code.tex -o ../output/big_data.pdf big_data.md --pdf-engine=xelatex

echo "Create complete.pdf"
pandoc -V geometry:a4paper -V geometry:margin=2cm --highlight-style pygments.theme --include-in-header inline_code.tex -o ../output/complete.pdf complete.md --pdf-engine=xelatex

echo "Create devops.pdf"
pandoc -V geometry:a4paper -V geometry:margin=2cm --highlight-style pygments.theme --include-in-header inline_code.tex -o ../output/devops.pdf devops.md --pdf-engine=xelatex

echo "Create ML.pdf"
pandoc -V geometry:a4paper -V geometry:margin=2cm --highlight-style pygments.theme --include-in-header inline_code.tex -o ../output/ml.pdf ML.md --pdf-engine=xelatex

