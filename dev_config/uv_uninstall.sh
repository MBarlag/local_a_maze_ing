uv cache clean 2>/dev/null
rm -rf "$(uv python dir 2>/dev/null)" 
rm -rf "$(uv tool dir 2>/dev/null)"
rm -f ~/.local/bin/uv ~/.local/bin/uvx
rm -rf ./.venv