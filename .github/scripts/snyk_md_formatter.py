import json

def color(text, color):
    return f'<span style="color:{color}">{text}</span>'

def bold(text):
    return f'**{text}**'

def section(title, color=None):
    if color:
        return f'### {color(bold(title), color)}\n'
    return f'### {bold(title)}\n'

def format_issue(issue):
    severity = issue.get('severity', '').lower()
    if severity == 'low':
        sev_str = color(bold('[Low]'), 'blue')
    elif severity == 'medium':
        sev_str = color(bold('[Medium]'), 'orange')
    elif severity == 'high':
        sev_str = color(bold('[High]'), '#8B0000')  # dark red
    elif severity == 'critical':
        sev_str = color(bold('[Critical]'), 'red')
    else:
        sev_str = bold('[Unknown]')
    out = [f"{sev_str} {bold(issue.get('title', ''))}"]
    if 'description' in issue:
        out.append(f"{color('Info:', 'green')} {issue['description']}")
    if 'rule' in issue:
        out.append(f"{color('Rule:', 'green')} {color(issue['rule'], 'green')}")
    if 'path' in issue:
        out.append(f"{color('Path:', 'green')} {color(issue['path'], 'green')}")
    if 'file' in issue:
        out.append(f"{color('File:', 'purple')} {color(issue['file'], 'purple')}")
    if 'resolve' in issue:
        out.append(f"{color('Resolve:', 'green')} {color(issue['resolve'], 'green')}")
    return '\n'.join(out)

def main():
    with open('snyk-iac-results.json') as f:
        data = json.load(f)

    md = []
    md.append(section('Snyk IaC Test Results', 'green'))
    md.append('\nSnyk Infrastructure as Code\n')
    md.append('* Snyk testing Infrastructure as Code configuration issues.\n  ✔ Test completed.\n')
    md.append('\n---\n\n')
    md.append('## Issues\n')

    issues = data.get('infrastructureAsCodeIssues', [])
    if not issues:
        md.append(color('✔ No issues found!', 'green'))
    else:
        sev_count = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for issue in issues:
            sev = issue.get('severity', '').lower()
            if sev in sev_count:
                sev_count[sev] += 1
        for sev in ['critical', 'high', 'medium', 'low']:
            if sev_count[sev]:
                sev_color = {'critical': 'red', 'high': '#8B0000', 'medium': 'orange', 'low': 'blue'}[sev]
                md.append(f"{color(bold(sev.capitalize() + ' Severity Issues:'), sev_color)} {sev_count[sev]}")
        md.append('\n')
        for issue in issues:
            md.append(format_issue(issue))
            md.append('\n')

    md.append('\n---\n\n')
    # Test Summary
    org = data.get('organization', 'Unknown')
    project = data.get('projectName', 'Unknown')
    md.append(f"{color(bold('Organization:'), 'green')} {color(org, 'green')}\n")
    md.append(f"{color(bold('Project name:'), 'orange')} {color(project, 'orange')}\n")

    files_without_issues = data.get('filesWithoutIssues', 0)
    files_with_issues = data.get('filesWithIssues', 0)
    ignored_issues = data.get('ignoredIssues', 0)
    total_issues = data.get('totalIssues', 0)

    md.append(f"{color('✔ Files without issues:', 'green')} {color(str(files_without_issues), 'green')}")
    md.append(f"{color('✗ Files with issues:', 'red')} {color(str(files_with_issues), 'red')}")
    md.append(f"{color('Ignored issues:', '#001F5B')} {color(str(ignored_issues), '#001F5B')}")
    # Total issues with color by severity
    if sev_count['critical']:
        total_color = 'red'
    elif sev_count['high']:
        total_color = '#8B0000'
    elif sev_count['medium']:
        total_color = 'orange'
    elif sev_count['low']:
        total_color = 'blue'
    else:
        total_color = 'purple'
    md.append(f"{color('Total issues:', 'purple')} {color(str(total_issues), total_color)}")

    with open('snyk-results.md', 'w') as f:
        f.write('\n'.join(md))

if __name__ == '__main__':
    main()