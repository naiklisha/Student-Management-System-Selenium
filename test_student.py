
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = "http://127.0.0.1:8000"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get(URL)
    yield browser
    browser.quit()


def add_student(driver, name, usn, course, email):
    driver.find_element(By.ID, "studentName").send_keys(name)
    driver.find_element(By.ID, "studentUSN").send_keys(usn)
    driver.find_element(By.ID, "studentCourse").send_keys(course)
    driver.find_element(By.ID, "studentEmail").send_keys(email)
    driver.find_element(By.ID, "addStudentBtn").click()


def test_page_load(driver):
    assert "Student Management System" in driver.title
    assert driver.find_element(By.ID, "studentForm").is_displayed()


def test_add_student(driver):
    add_student(driver, "Rahul", "1STU101", "AI & Robotics", "rahul@test.com")
    assert "Student added successfully!" in driver.find_element(By.ID, "message").text
    assert "Rahul" in driver.find_element(By.ID, "studentTableBody").text


def test_duplicate_usn_validation(driver):
    add_student(driver, "Rahul", "1STU101", "AI & Robotics", "rahul@test.com")
    add_student(driver, "Amit", "1STU101", "Computer Science", "amit@test.com")

    assert "Student USN already exists!" in driver.find_element(By.ID, "message").text


def test_delete_student(driver):
    add_student(driver, "Rahul", "1STU101", "AI & Robotics", "rahul@test.com")
    driver.find_element(By.CLASS_NAME, "delete-btn").click()

    assert driver.find_element(By.ID, "studentTableBody").text == ""
    assert "Total Students: 0" in driver.find_element(By.ID, "studentCount").text


def test_student_count(driver):
    add_student(driver, "Rahul", "1STU101", "AI & Robotics", "rahul@test.com")
    assert "Total Students: 1" in driver.find_element(By.ID, "studentCount").text
