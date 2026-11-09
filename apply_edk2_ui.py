from pathlib import Path

files = {
    "gui/theme/common/portrait.xml": (
        '<button style="main_button_half_height">',
        '%indent%', '%row21a_y%', 'main_button_half_height'
    ),
    "gui/theme/common/landscape.xml": (
        '<button style="main_button_half_width">',
        '%col1_x_left%', '%row15a_y%', 'main_button_half_width'
    )
}

for filename, (style, x, y, _) in files.items():
    p = Path(filename)
    s = p.read_text()

    start = s.index('<page name="advanced">')
    end = s.index('\n\t\t</page>', start)
    section = s[start:end]

    if 'name="EDK2 Launcher (not enabled)"' in section:
        print(filename, ": déjà adapté")
        continue

    item = (
        '\t\t\t\t<listitem name="EDK2 Launcher (not enabled)">\n'
        '\t\t\t\t\t<action function="page">edk2_status</action>\n'
        '\t\t\t\t</listitem>\n'
    )
    pos = section.rfind('\t\t\t</listbox>')
    if pos < 0:
        raise RuntimeError("Liste Advanced introuvable: " + filename)

    section = section[:pos] + item + section[pos:]
    s = s[:start] + section + s[end:]

    button = (
        f'\t\t\t<button style="{style}">\n'
        f'\t\t\t\t<placement x="{x}" y="{y}"/>\n'
        '\t\t\t\t<text>Back to Advanced</text>\n'
        '\t\t\t\t<action function="page">advanced</action>\n'
        '\t\t\t</button>'
    )

    page = f'''
\t\t<page name="edk2_status">
\t\t\t<template name="page"/>

\t\t\t<text style="text_l">
\t\t\t\t<placement x="%col1_x_header%" y="%row3_header_y%"/>
\t\t\t\t<text>EDK2 Launcher</text>
\t\t\t</text>

\t\t\t<text style="text_m_fail">
\t\t\t\t<placement x="%center_x%" y="%row7_y%" placement="5"/>
\t\t\t\t<text>Launcher is not enabled yet.</text>
\t\t\t</text>

\t\t\t<text style="text_m">
\t\t\t\t<placement x="%center_x%" y="%row8_y%" placement="5"/>
\t\t\t\t<text>BootShim must be loaded by the bootloader.</text>
\t\t\t</text>

\t\t\t<text style="text_m">
\t\t\t\t<placement x="%center_x%" y="%row9_y%" placement="5"/>
\t\t\t\t<text>TWRP cannot safely execute it directly.</text>
\t\t\t</text>

\t\t\t<text style="text_m">
\t\t\t\t<placement x="%center_x%" y="%row10_y%" placement="5"/>
\t\t\t\t<text>No boot, recovery or vbmeta partition is modified.</text>
\t\t\t</text>

{button}

\t\t\t<action>
\t\t\t\t<touch key="back"/>
\t\t\t\t<action function="page">advanced</action>
\t\t\t</action>
\t\t</page>
'''
    marker = '\n\t\t<page name="partsdcardsel">'
    if marker not in s:
        raise RuntimeError("Page d'insertion introuvable: " + filename)

    s = s.replace(marker, '\n' + page + marker, 1)
    p.write_text(s)
    print(filename, ": modifié")
