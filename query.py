import client
import csv
import logging
import pprint
import reports
import sys
import utils

from args import parser as argparser

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(stream=sys.stderr))
logger.setLevel(logging.DEBUG)


def find_check_for_id(checks, check_id):
    for check in checks:
        if check.id == check_id:
            return check
    else:
        raise Exception(
            'Unable to find check for check_id {}'.format(check_id)
        )


def get_alarm_reports(driver, filter=None):
    """Use the overview to map all alarms to entities in single api call.

    The overview returns a list of rows.
    Each row in overview is a dictionary consiting of:
       entity: <entity_obj>
       alarms: [<alarm_obj_1>, <alarm_obj_2>, ..., <alarm_obj_n>]
       checks: [<check_obj_1, <check_obj_2>, ..., <check_obj_n>]

    :param driver: Rackspace Monitoring driver instance
    :type driver: RackspaceMonitoringDriver
    :param filter: Function to filter alarms
    :type filter: function|lambda
    :returns: List of (entity_obj, check_obj, alarm_obj) pairs.
    :rtype: list of tuples
    """
    report_list = []
    overview = driver.ex_views_overview()

    # Iterate over each row. Pair entity objects with targeted alarms
    for row in overview:
        for alarm in row.get('alarms'):
            if filter is None or filter(alarm):
                report_list.append(reports.Alarm(
                    row['entity'],
                    find_check_for_id(row['checks'], alarm.check_id),
                    alarm
                ))
    return report_list


if __name__ == '__main__':

    args = argparser.parse_args()
    start = utils.datetime_to_timestamp(args.start)
    stop = utils.datetime_to_timestamp(args.stop)
    driver = client.get_instance()
    alarm_reports = get_alarm_reports(
        driver,
        filter=lambda a: a.label.startswith('rally_')
    )

    columns = [
        'entity_id',
        'entity_label',
        'check_id',
        'check_label',
        'alarm_label',
        'alarm_id',
        'valid',
        'state',
        'duration',
        'start',
        'stop'
    ]
    with open(args.output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, columns)
        writer.writeheader()

        for alarm_report in alarm_reports:
            logger.debug(
                "Checking history for entity: {} and alarm: {}"
                .format(alarm_report.entity.id, alarm_report.alarm.id)
            )
            for row in alarm_report.run(start, stop):
                logger.debug(pprint.pformat(row))
                writer.writerow(row)
