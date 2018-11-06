import pprint
from datetime import datetime, date
import re

rows = [
    dict(
        pid='a',
        gameend_datetime='2018-08-10 01:01:01',
        arr_item='1-100-10, 2-100-2, 2-200-3, 1-100-2'
    ),
    dict(
        pid='a',
        gameend_datetime='2018-08-10 02:01:01',
        arr_item='1-100-3, 2-100-4, 2-201-3, 1-101-2'
    ),
    dict(
        pid='a',
        gameend_datetime='2018-08-11 02:01:01',
        arr_item='1-100-3, 2-100-4, 2-201-3, 1-101-2'
    ),
    dict(
        pid='b',
        gameend_datetime='2018-08-10 01:01:01',
        arr_item='1-100-8, 2-100-1, 2-200-5, 1-100-3'
    ),
    dict(
        pid='b',
        gameend_datetime='2018-08-10 02:01:01',
        arr_item='1-100-3, 1-120-4, 2-201-3, 1-101-2'
    ),
    dict(
        pid='b',
        gameend_datetime='2018-08-11 02:01:01',
        arr_item='1-100-3, 1-121-2, 2-201-3, 1-101-2'
    ),
]
getitem_dict = {}
for row in rows:
    pid = row['pid']
    # date = row['gameend_datetime']
    date = datetime.strptime(row['gameend_datetime'], '%Y-%m-%d %H:%M:%S').date().strftime('%Y%m%d')
    arr_item = row['arr_item']
    if pid not in getitem_dict:

        getitem_dict[pid] = dict()
    if date not in getitem_dict[pid]:
        getitem_dict[pid][date] = dict(
            first_split=[],
            second_split=[],
            getitem=dict()
        )

    getitem_dict[pid][date]['first_split'] += arr_item.split(',')
    if pid in getitem_dict and date in getitem_dict[pid]:
        for first_index in range(len(getitem_dict[pid][date]['first_split'])):
            print(getitem_dict[pid][date]['first_split'][first_index])

# for pid in getitem_dict:
#     for date in getitem_dict[pid]:
#         getitem_dict[pid][date]
    # getitem_dict2 = dict()
    # for item_list in getitem_dict[pid][date]['first_split']:
    #     if pid not in getitem_dict2:
    #         getitem_dict2[pid] = dict()
    #     if date not in getitem_dict2[pid]:
    #         getitem_dict2[pid][date] = dict(
    #             second_split=[]
    #         )
    #     getitem_dict2[pid][date]['second_split'].append(item_list.split('-'))
# for pid in getitem_dict:
#     for date in getitem_dict[pid]:
#         for first_split in getitem_dict[pid][date]:
#             for first_list in getitem_dict[pid][date][first_split]:
#                 # print(str(first_list))
#                 getitem_dict[pid][date]['second_split'].append(str(first_list).split('-'))

# for pid in getitem_dict:
#     for date in getitem_dict[pid]:
#         for second_split in getitem_dict[pid][date]:
#             for second_list in getitem_dict[pid][date]['second_split']:
#                 if second_list[1] not in getitem_dict[pid][date]['getitem']:
#                     getitem_dict[pid][date]['getitem'][second_list[1]] = dict()
#                 if second_list[0] not in getitem_dict[pid][date]['getitem'][second_list[1]]:
#                     getitem_dict[pid][date]['getitem'][second_list[1]][second_list[0]] = 0
#                 if [second_list[1]] in getitem_dict[pid][date]:
#                     if second_list[0] in getitem_dict[pid][date]['getitem'][second_list[1]]:
#                         getitem_dict[pid][date]['getitem'][second_list[1]][second_list[0]] += int([second_list[2]])



                # print(first_list.split('-'))



    # for item_list in getitem_dict[pid][date]['first_split']:
    #     getitem_dict[pid][date]['second_split'].append(item_list.split('-'))
    #     # getitem_dict[pid][date]['second_split'].append(getitem_dict[pid][date]['first_split'].split('-'))



pprint.pprint(getitem_dict)
