/***
* N8, An amalgamation of personal code
* Copyright (C) 2024 Nathaniel Wright
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
***/

// On page load or when changing themes, best to add inline in `head` to avoid FOUC
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
    localStorage.theme = 'dark'
} else {
    document.documentElement.classList.remove('dark')
    localStorage.theme = 'light'
}

function changeToDarkMode() {
    localStorage.theme = 'dark'
    document.documentElement.classList.add('dark')
}

function changeToLightMode() {
    localStorage.theme = 'light'
    document.documentElement.classList.remove('dark')
}

function toggleTheme() {
    if (localStorage.theme == 'light') {
        changeToDarkMode()
    }
    else {
        changeToLightMode()
    }
}

function respectOSTheme() {
    localStorage.removeItem('theme')
}