def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 !=1
    
    
def test_isInstance():
    assert isinstance('my name is pritesh', str)
    assert not isinstance('10', int)
    

class Student:
    def __init__(self, first:str, last:str, major:str, years:int) -> None:
        self.first = first
        self.last = last
        self.major = major
        self.years = years
        
import pytest

@pytest.fixture
def default_student():
    return Student('Pritesh','Surale','ECE',4)


def test_class(default_student):
    assert default_student.first == 'Pritesh', 'first should be pritesh'
    assert default_student.last == 'Surale'
    assert default_student.major == 'ECE'
    assert default_student.years == 4
    
