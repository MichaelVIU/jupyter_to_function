# Configuration file for jupyter-notebook.

def scrub_output_pre_save(path, model, contents_manager, **kwargs):
    """scrub output before saving notebooks"""
    # only run on notebooks
    log = contents_manager.log
    ignore_line_contains = ['show(', 'head(', 'display(']

    filename = path.replace('ipynb', 'py')   # Generate py filename

    py_file = open(filename, 'w')   # Open File in write override Mode

    if model['type'] != 'notebook':
        return
    # only run on nbformat v4
    if model['content']['nbformat'] != 4:
        return

    function_start = False

    for cell in model['content']['cells']:  # loop through each cell
        # if markdown row contains pycreatefunction set tab line to true and save line in file
        if cell['cell_type'] == 'markdown' and 'pycreatefunction' in cell['source']:
            py_file.write("%s\n" % cell['source'])
            function_start = True
        elif (cell['cell_type'] == 'code') and function_start:
            for row in cell['source'].splitlines():  # if code is multiline
                if not any(ig in row for ig in ignore_line_contains):
                    py_file.write("    %s\n" % row)

    log.info("Saving file as function: %s" % filename)
    py_file.close()

c.FileContentsManager.pre_save_hook = scrub_output_pre_save