import io
import os
from jinja2 import Template


def gen_html_report(summary):
    """ render html report with specified report name and template

    Args:
        summary (dict): test result summary data
        report_template (str): specify html report template path, template should be in Jinja2 format.
        report_dir (str): specify html report save directory
        report_file (str): specify html report file path, this has higher priority than specifying report dir.
    """

    report_template = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "template.html"
    )

    # start_at_timestamp = summary["time"]["start_at"]
    # summary["time"]["start_datetime"] = start_at_timestamp

    with io.open(report_template, "r", encoding='utf-8') as fp_r:
        template_content = fp_r.read()
        rendered_content = Template(
            template_content,
            extensions=["jinja2.ext.loopcontrols"]
        ).render(summary)
        return rendered_content



