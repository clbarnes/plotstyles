import json
from nbformat import current as nbf
from matplotlib import pyplot as plt
# import subprocess

template_path = 'templates/template.ipynb'
output_path = 'plotstyles.ipynb'
nb = nbf.new_notebook()

with open(template_path) as f:
    template = json.load(f)

out_cells = []

for cell in template['cells']:
    cell_type = cell['cell_type']
    source = cell['source']
    if cell_type == 'markdown':
        out_cells.append(nbf.new_text_cell('markdown', source))
    else:
        out_cells.append(nbf.new_code_cell(source))


def make_title(s):
    return s.replace('-', ' ').replace('_', ' ').title()


for style_str in sorted(plt.style.available):
    out_cells.append(nbf.new_text_cell('markdown', "### {} (`'{}'`)".format(make_title(style_str), style_str)))
    out_cells.append(nbf.new_code_cell(
        """\
with plt.style.context(('{0}')):
    make_plots('{0}')\
        """.format(style_str).splitlines(keepends=True)
    ))

nb['worksheets'].append(nbf.new_worksheet(cells=out_cells))

with open(output_path, 'w') as f:
    nbf.write(nb, f, 'ipynb')

# subprocess.call(["ipython", "-c", "%run {}".format(filename)])
