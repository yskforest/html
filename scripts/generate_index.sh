#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <target_directory>"
    exit 1
fi

target_dir="$1"
cd "$target_dir" || { echo "Cannot enter $target_dir"; exit 1; }

output_file="index.html"

# HTML header
cat <<EOF > "$output_file"
<html>
<head>
    <meta charset="UTF-8">
    <title>Index</title>
</head>
<body>
    <h1>HTML File List</h1>
    <ul>
EOF

# パイプを使わずに for で処理する（日本語・空白対応）
# IFSのままではスペース区切りになるのでnull分離で処理
while IFS= read -r -d '' file; do
    # ファイル名から ./ を除去
    relpath="${file#./}"
    printf '        <li><a href="%s">%s</a></li>\n' "$relpath" "$relpath" >> "$output_file"
    echo "$relpath"
done < <(find . -type f -name "*.html" ! -name "index.html" -print0)

# HTML footer
cat <<EOF >> "$output_file"
    </ul>
</body>
</html>
EOF

echo "Done: index.html created in $target_dir"
