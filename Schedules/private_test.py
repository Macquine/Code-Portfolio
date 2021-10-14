import numpy as np
import typing
import unittest

from schedule import Schedule


class ScheduleFactory(object):
    @staticmethod
    def get_schedule_three_tracks() -> Schedule:
        courses = {
            'A': [1,2],
            'B': [0],
            'C': [1],
            'D': [0],
            'E': [1,0],
            'F': [1],
            'G': [1,0],
            'H': [1,0],
            'I': [1],
            'J': [0,1],
            'K': [2],
            'L': [2],
        }
        schedule = Schedule(n_weekdays=3, n_slots_day= 4, n_tracks=3,
                            n_rooms=3, courses=courses)
        return schedule

    @staticmethod
    def get_schedule_2() -> Schedule:
        courses = {
            'A': [1,2],
            'B': [0],
            'C': [1],
            'D': [0],
            'E': [1,0],
            'F': [1],
            'G': [1,0],
            'H': [1,0],
            'I': [1],
            'J': [0,1],
            'K': [2],
            'L': [2],
            'M': [2],
            'N': [2],
            'O': [0],
            'P': [0],
            'Q': [0],
            'R': [0],
            'S': [1],
            'T': [1],
            'U': [1],
            'V': [1],
        }
        schedule = Schedule(n_weekdays= 3, n_slots_day= 4, n_tracks=3,
                            n_rooms=2, courses=courses)
        return schedule

class TestSchedule(unittest.TestCase):
    def violatesrules(self,schedule: Schedule) -> bool:
        """Checks whether the 'given schedule' violates one of the following conditions:
        - There is at most one interval hour for each track.
        - Two courses that are offered to the same track are not offered in the same time slot.

        Returns: True if one of these conditions is violated, False otherwise.
        """
        # print(schedule.schedule)
        for day in range(schedule.n_weekdays):
            for track in range(schedule.n_tracks):
                if schedule.count_intervals_on_day(day, track) > 1:
                    return True
                for slot in range(schedule.n_slots_day):
                    if schedule.duplicate_track_courses_on_slot(day, slot, track):
                        return True
        return False

    def final_check(self, schedule: Schedule) -> bool:
        """ Determines if a track has atleast 2 courses on a day when it has a course on a day.
        Returns: A boolean, True if the schedule has at least two courses on a day
        the track has courses, False otherwise. """
        for day in range(schedule.n_weekdays):
            for track in range(schedule.n_tracks):
                if schedule.count_courses_on_day(day, track) < 2 and schedule.count_courses_on_day(day, track) != 0: 
                    return False

        return True 
    
    def _check_solution(self, schedule: Schedule, result: np.array):
        self.assertIsNotNone(result)
        result_flat = result.flatten()
        result_flat = np.delete(result_flat, np.where(result_flat == ''))
        # no duplicates
        self.assertEqual(len(np.unique(result_flat)), len(result_flat))
        # all courses
        self.assertSetEqual(set(result_flat), set(schedule.courses.keys()))

        for day in range(schedule.n_weekdays):
            for track in range(schedule.n_tracks):
                self.assertNotEqual(schedule.count_courses_on_day(day, track), 1)
                self.assertLessEqual(schedule.count_intervals_on_day(day, track), 1)

                for slot in range(schedule.n_slots_day):
                    self.assertFalse(schedule.duplicate_track_courses_on_slot(day, slot, track))

    def test_build_schedule_adverserial_backtracking_greedy(self): #Unittest 1
        #Test case that does not hold an optimal schedule when attempting greedy.
        schedule_backtracking = ScheduleFactory.get_schedule_three_tracks()
        schedule_greedy = ScheduleFactory.get_schedule_three_tracks()
        result_backtracking = schedule_backtracking.build_schedule_backtracking()
        schedule_greedy.build_schedule_greedy()
        self._check_solution(schedule_backtracking, result_backtracking) #Checks if backtracking is optimal.
        #Checks if greedy schedule is not optimal while the backtracking schedule is optimal. 
        self.assertNotEqual(schedule_greedy.final_check(), schedule_backtracking.final_check()) 

    def test_build_schedule_backtracking(self): #Unittest 2
        #Test case that test 21 courses for backtracking
        schedule_backtracking = ScheduleFactory.get_schedule_2()
        result_backtracking = schedule_backtracking.build_schedule_backtracking() #Builds the schedule with the backtracking method.
        self._check_solution(schedule_backtracking, result_backtracking) #Checks if the result is valid.
    
    def test_build_schedule_greedy(self): #Unittest 3
        #Test case that test 21 courses for greedy without the final check.
        schedule_greedy = ScheduleFactory.get_schedule_2()
        schedule_greedy.build_schedule_greedy() #Builds the schedule with the greedy method.
        self.assertFalse(schedule_greedy.violatesrules()) #Checks if the result complies to the rules specified in the violaterules() method.