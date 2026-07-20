#compdef nexus nexus-backup nexus-calendar nexus-contacts nexus-cookbook nexus-docs nexus-gallery nexus-mail nexus-mcp nexus-memory nexus-notes nexus-personal nexus-preset nexus-research nexus-sessions nexus-signature nexus-skills nexus-tasks nexus-theme nexus-webhook
# Zsh tab-completion for the nexus umbrella + sub-CLIs.
#
# Drop in any directory on $fpath, e.g.:
#     fpath=(/path/to/nexus-ui/scripts/_completion $fpath)
#     autoload -U compinit; compinit
#
# Then `nexus <tab>` completes subcommands; `nexus mail <tab>`
# completes mail subcommands; `nexus-mail <tab>` works the same.

_nexus_scripts_dir() {
    local self="${(%):-%x}"
    while [[ -L "$self" ]]; do self="$(readlink "$self")"; done
    cd "${self:h}/.." && pwd
}

typeset -gA _nexus_subs

_nexus_refresh() {
    _nexus_subs=()
    local dir="$(_nexus_scripts_dir)"
    local py="$dir/../venv/bin/python"
    [[ -x "$py" ]] || py="$(command -v python3)"
    local f sub help_out commands
    for f in "$dir"/nexus-*; do
        [[ -x "$f" ]] || continue
        case "$f" in
            *.bak|*.pyc|*.pre-*) continue ;;
        esac
        sub="${${f:t}#nexus-}"
        help_out=$("$py" "$f" --help 2>/dev/null) || continue
        commands=$(echo "$help_out" | grep -oE '\{[a-z0-9_,-]+\}' | head -1 \
            | tr -d '{}' | tr ',' ' ')
        _nexus_subs[$sub]="$commands"
    done
}

_nexus() {
    [[ ${#_nexus_subs} -eq 0 ]] && _nexus_refresh

    local cmd="${words[1]}"

    if [[ "$cmd" == "nexus" ]]; then
        if (( CURRENT == 2 )); then
            local -a subs=(${(k)_nexus_subs} help)
            _describe 'subcommand' subs
            return
        fi
        local sub="${words[2]}"
        if [[ "$sub" == "help" ]] && (( CURRENT == 3 )); then
            local -a subs=(${(k)_nexus_subs})
            _describe 'subcommand' subs
            return
        fi
        if (( CURRENT == 3 )); then
            local -a sc=(${(s/ /)_nexus_subs[$sub]})
            _describe 'command' sc
            return
        fi
        return
    fi

    # nexus-foo <tab>
    local sub="${cmd#nexus-}"
    if (( CURRENT == 2 )); then
        local -a sc=(${(s/ /)_nexus_subs[$sub]})
        _describe 'command' sc
        return
    fi
}

_nexus "$@"
