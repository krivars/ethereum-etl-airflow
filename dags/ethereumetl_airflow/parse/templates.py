import os

from eth_utils import event_abi_to_log_topic, function_abi_to_4byte_selector

from ethereumetl_airflow.utils.template_utils import render_template


def render_parse_udf_template(
        sqls_folder,
        parser_type,
        **kwargs
):
    template = get_parse_udf_template(parser_type, sqls_folder)
    rendered_template = render_template(template, kwargs)

    return rendered_template


def render_parse_sql_template(
        sqls_folder,
        parser_type,
        parser,
        **kwargs
):
    template = get_parse_sql_template(parser_type, sqls_folder)
    selector = abi_to_selector(parser_type, parser['abi'])
    rendered_template = render_template(template, dict(kwargs, parser=parser, selector=selector))

    return rendered_template


def render_merge_template(
        sqls_folder,
        **kwargs
):
    template = get_merge_table_sql_template(sqls_folder)

    rendered_template = render_template(template, kwargs)

    return rendered_template


def get_parse_udf_template(parser_type, sqls_folder):
    if parser_type == 'log':
        filename = 'parse_logs_udf.sql'
    else:
        filename = 'parse_traces_udf.sql'

    filepath = os.path.join(sqls_folder, filename)

    with open(filepath) as file_handle:
        content = file_handle.read()
        return content


def get_parse_sql_template(parser_type, sqls_folder):
    if parser_type == 'log':
        filename = 'parse_logs.sql'
    else:
        filename = 'parse_traces.sql'

    filepath = os.path.join(sqls_folder, filename)

    with open(filepath) as file_handle:
        content = file_handle.read()
        return content



def get_merge_table_sql_template(sqls_folder):
    filepath = os.path.join(sqls_folder, 'merge_table.sql')
    with open(filepath) as file_handle:
        content = file_handle.read()
        return content


def abi_to_selector(parser_type, abi):
    if parser_type == 'log':
        return '0x' + event_abi_to_log_topic(abi).hex()
    else:
        return '0x' + function_abi_to_4byte_selector(abi).hex()


def replace_refs(contract_address, ref_regex, project_id, dataset_name):
    return ref_regex.sub(
        r"`{project_id}.{dataset_name}.\g<1>`".format(
            project_id=project_id, dataset_name=dataset_name
        ), contract_address)
