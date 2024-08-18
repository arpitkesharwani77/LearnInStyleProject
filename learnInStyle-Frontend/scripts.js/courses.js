import { fetchAPI } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const courses = await fetchAPI('/courses/');
    
    const courseList = document.getElementById('course-list');
    courseList.innerHTML = '';
    courses.forEach(course => {
        const courseItem = document.createElement('div');
        courseItem.className = 'course-item';
        courseItem.innerHTML = `<h2>${course.title}</h2><p>${course.description}</p>`;
        courseList.appendChild(courseItem);
    });
});
