#!/bin/bash
# Generate docs.md
# requires pydoc-markdown 4.5.0
config=$(cat <<'EOF'
{
    "processors": [
        {
            "type": "filter",
            "expression":"not name ==\"info\" and default()"
        },
        {
            "type": "pydocmd"
        }
    ],
    "renderer": {
        "type": "markdown",
        "render_toc": true
    }
}
EOF
)

cd jc
echo Building docs for: package
pydoc-markdown -m jc "${config}" > ../docs/readme.md
sed -i "" 's/^#### /### /g' ../docs/readme.md

echo Building docs for: lib
pydoc-markdown -m jc.lib "${config}" > ../docs/lib.md
sed -i "" 's/^#### /### /g' ../docs/lib.md

echo Building docs for: utils
pydoc-markdown -m jc.utils "${config}" > ../docs/utils.md
sed -i "" 's/^#### /### /g' ../docs/utils.md

echo Building docs for: universal parser
pydoc-markdown -m jc.parsers.universal "${config}" > ../docs/parsers/universal.md
sed -i "" 's/^#### /### /g' ../docs/parsers/universal.md

# a bit of inception here... jc is being used to help
# automate the generation of its own documentation. :)

# pull jc parser objects into a bash array from jq
# filter out any plugin parsers
parsers=()
while read -r value
do
    parsers+=("$value")
done < <(jc -a | jq -c '.parsers[] | select(.plugin != true)')

for parser in "${parsers[@]}"
do
    parser_name=$(jq -r '.name' <<< "$parser")
    compatible=$(jq -r '.compatible | join(", ")' <<< "$parser")
    version=$(jq -r '.version' <<< "$parser")
    author=$(jq -r '.author' <<< "$parser")
    author_email=$(jq -r '.author_email' <<< "$parser")

    echo "Building docs for: ${parser_name}"
    echo "[Home](https://kellyjonbrazil.github.io/jc/)" > ../docs/parsers/"${parser_name}".md
    pydoc-markdown -m jc.parsers."${parser_name}" "${config}" >> ../docs/parsers/"${parser_name}".md
    echo "### Parser Information" >> ../docs/parsers/"${parser_name}".md
    echo "Compatibility:  ${compatible}" >> ../docs/parsers/"${parser_name}".md
    echo >> ../docs/parsers/"${parser_name}".md
    echo "Version ${version} by ${author} (${author_email})" >> ../docs/parsers/"${parser_name}".md
    sed -i "" 's/^#### /### /g' ../docs/parsers/"${parser_name}".md
done
