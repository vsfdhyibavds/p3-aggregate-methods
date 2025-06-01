import unittest
from datetime import datetime, timedelta
from lib.enrollment import Student, Course, Enrollment

class TestAggregateMethods(unittest.TestCase):

    def setUp(self):
        # Create students and courses
        self.student1 = Student("Alice")
        self.student2 = Student("Bob")
        self.course1 = Course("Math")
        self.course2 = Course("Science")

        # Enroll students in courses
        self.student1.enroll(self.course1)
        self.student1.enroll(self.course2)
        self.student2.enroll(self.course1)

        # Assign grades for student1
        for enrollment in self.student1.get_enrollments():
            self.student1._grades[enrollment] = 90

        # Assign grades for student2
        for enrollment in self.student2.get_enrollments():
            self.student2._grades[enrollment] = 80

        # Clear Enrollment.all and add enrollments with specific dates for testing aggregate_enrollments_per_day
        Enrollment.all.clear()
        # Create enrollments with specific dates
        e1 = Enrollment(self.student1, self.course1)
        e1._enrollment_date = datetime.now() - timedelta(days=1)
        # Enrollment.all.append(e1)  # Removed manual append

        e2 = Enrollment(self.student1, self.course2)
        e2._enrollment_date = datetime.now()
        # Enrollment.all.append(e2)  # Removed manual append

        e3 = Enrollment(self.student2, self.course1)
        e3._enrollment_date = datetime.now()
        # Enrollment.all.append(e3)  # Removed manual append

    def test_course_count(self):
        self.assertEqual(self.student1.course_count(), 2)
        self.assertEqual(self.student2.course_count(), 1)

    def test_aggregate_average_grade(self):
        self.assertEqual(self.student1.aggregate_average_grade(), 90)
        self.assertEqual(self.student2.aggregate_average_grade(), 80)

    def test_aggregate_enrollments_per_day(self):
        counts = Enrollment.aggregate_enrollments_per_day()
        today = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=1)).date()
        self.assertEqual(counts[today], 2)
        self.assertEqual(counts[yesterday], 1)

if __name__ == "__main__":
    unittest.main()
