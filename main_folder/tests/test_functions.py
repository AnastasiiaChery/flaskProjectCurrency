from main_folder.functions import data_filter
from unittest.mock import Mock

# ?????????????????????????????
# @pytest.fixture()
# def tasks_db(tmpdir):
#     # Setup : start db
#     tasks.start_tasks_db(str(tmpdir), 'tiny')
#
#     yield  # здесь происходит тестирование
#
#     # Teardown : stop db
#     tasks.stop_tasks_db()

# @pytest.mark.parametrize('task',
#                          [Task('sleep', done=True),
#                           Task('wake', 'brian'),
#                           Task('breathe', 'BRIAN', True),
#                           Task('exercise', 'BrIaN', False)])
# def test_add_2(task):
#     task_id = tasks.add(task)
#     t_from_db = tasks.get(task_id)
#     assert equivalent(t_from_db, task)


def test_data_filter():
    t1 = data_filter(selected_date='2021913')
    t2 = data_filter(selected_date='20211027')
    t3 = data_filter(selected_date='20201027')
    t4 = data_filter(selected_date=None)
    assert len(t1) == 60
    assert len(t2) == 60
    assert t3 == []
    assert len(t4) == 60

# base_currency()
# data_filter()
# curr_hisrory()
# selected_df()
# curr_min()
# curr_max()
# curr_mean()
# converter()
