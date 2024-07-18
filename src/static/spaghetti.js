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