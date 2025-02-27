// Элементы интерфейса
const desktop = document.getElementById('desktop');
const desktopMenu = document.getElementById('desktopMenu');
const itemMenu = document.getElementById('itemMenu');
const menuCreate = document.getElementById('menuCreate');
const submenuCreate = document.getElementById('submenuCreate');
const awardsPanel = document.getElementById('awardsPanel'); // Панель наград

const dialogOverlay = document.getElementById('dialogOverlay');
const dialogTitle = document.getElementById('dialogTitle');
const dialogMessage = document.getElementById('dialogMessage');
const dialogInput = document.getElementById('dialogInput');
const dialogButtons = document.getElementById('dialogButtons');

// Элементы помощника
const assistantOverlay = document.getElementById('assistantOverlay');
const assistantText = document.getElementById('assistantText');

console.log("Script initialization started");

// Объект с инструкциями для наград
const rewardInstructions = {
    "Бейджик Инициации": "Поздравляю! Ты получил Бейджик Инициации за успешное прохождение первого этапа. Теперь начинается интерактивное испытание 'Операция Инициатива'. На твоём виртуальном рабочем столе спрятан секретный файл 'Initiative.txt'. Твоя задача – найти и открыть его, чтобы получить дальнейшие указания. Используй всё, что узнал на этапе знакомства с Astra Linux!",
    "Токен Командной Строки": "На этапе 2 ты научился работать в терминале. Теперь попробуй выполнить команду 'ls' и изучи структуру файловой системы. Для вызова терминала используй сочетание клавиш 'ALT+T'.",
    "Файл Знаний": "На этапе 3 ты собрал фрагменты документации. Твое задание: составь краткий конспект прочитанного материала.",
    "Щит Безопасности": "На этапе 4 ты узнал об инструментах защиты. Теперь попробуй настроить файрволл и просмотреть логи безопасности.",
    "Ключ Настройки": "На этапе 5 ты научился менять конфигурации системы. Твое задание: отредактируй конфигурационный файл и проверь результат.",
    "Оптимизирующий Бейдж": "На этапе 6 ты изучил методы оптимизации. Теперь оптимизируй работу системы, отключив неиспользуемые сервисы."
};

// Переменная для выбранной иконки
let selectedIcon = null;

// Счётчики для создаваемых объектов
let folderCount = 0;
let fileCount = 0;
let shortcutCount = 0;
let libreDrawCount = 0;
let librePresentCount = 0;
let libreSheetCount = 0;
let libreDocCount = 0;

// Инициализация: назначение обработчиков для уже существующих иконок и панели наград
document.addEventListener('DOMContentLoaded', () => {
    initIconsEvents();
    initAwards(); // Инициализация наград

    // Проверяем, выполнено ли задание по токену (если да – подсвечиваем награду)
    if (localStorage.getItem("terminalTokenCompleted") === "true") {
         const tokenAward = document.querySelector('[data-award="Токен Командной Строки"]');
         if (tokenAward) {
             tokenAward.classList.add("correct");
         }
         localStorage.removeItem("terminalTokenCompleted");
    }
});

/* ========== МЕНЮ РАБОЧЕГО СТОЛА ========== */
// При правом клике на пустой области рабочего стола
desktop.addEventListener('contextmenu', function (e) {
    const iconEl = e.target.closest('.icon');
    if (!iconEl) {
        e.preventDefault();
        if (selectedIcon) {
            selectedIcon.classList.remove('selected');
            selectedIcon = null;
        }
        hideAllMenus();
        showDesktopMenu(e.clientX, e.clientY);
    }
});

// Скрывать меню при клике вне их области
document.addEventListener('click', function (e) {
    if (!desktopMenu.contains(e.target)) {
        hideAllMenus();
    }
    if (!itemMenu.contains(e.target)) {
        itemMenu.style.display = 'none';
    }
});

// Появление подменю «Создать» при наведении
menuCreate.addEventListener('mouseenter', function () {
    showSubmenuCreate();
});
menuCreate.addEventListener('mouseleave', function () {
    submenuCreate.style.display = 'none';
});

// Функция отображения контекстного меню рабочего стола с учетом границ окна
function showDesktopMenu(x, y) {
    desktopMenu.style.display = 'block';
    desktopMenu.style.left = x + 'px';
    desktopMenu.style.top = y + 'px';
    const dmRect = desktopMenu.getBoundingClientRect();
    if (dmRect.right > window.innerWidth) {
        desktopMenu.style.left = (window.innerWidth - dmRect.width - 10) + 'px';
    }
    if (dmRect.bottom > window.innerHeight) {
        desktopMenu.style.top = (window.innerHeight - dmRect.height - 10) + 'px';
    }
}

// Функция отображения подменю "Создать"
function showSubmenuCreate() {
    submenuCreate.style.display = 'block';
    submenuCreate.style.left = '100%';
    submenuCreate.style.top = '0';
    const subRect = submenuCreate.getBoundingClientRect();
    if (subRect.right > window.innerWidth) {
        submenuCreate.style.left = -subRect.width + 'px';
    }
    if (subRect.bottom > window.innerHeight) {
        let diff = subRect.bottom - window.innerHeight + 10;
        submenuCreate.style.top = -diff + 'px';
    }
}

// Функция отображения меню предмета (иконки)
function showItemMenu(x, y) {
    itemMenu.style.display = 'block';
    itemMenu.style.left = x + 'px';
    itemMenu.style.top = y + 'px';
    const imRect = itemMenu.getBoundingClientRect();
    if (imRect.right > window.innerWidth) {
        itemMenu.style.left = (window.innerWidth - imRect.width - 10) + 'px';
    }
    if (imRect.bottom > window.innerHeight) {
        itemMenu.style.top = (window.innerHeight - imRect.height - 10) + 'px';
    }
}

// Функция скрытия всех меню
function hideAllMenus() {
    desktopMenu.style.display = 'none';
    submenuCreate.style.display = 'none';
    itemMenu.style.display = 'none';
}

/* ========== ДЕЙСТВИЯ С ПРЕДМЕТОМ ========== */
function onIconLeftClick(e) {
    if (selectedIcon && selectedIcon !== this) {
        selectedIcon.classList.remove('selected');
        selectedIcon.classList.remove('expanded');
    }
    selectedIcon = this;
    selectedIcon.classList.add('selected');

    // Переключаем класс 'expanded' для текущей иконки
    if (selectedIcon.classList.contains('expanded')) {
        selectedIcon.classList.remove('expanded');
    } else {
        selectedIcon.classList.add('expanded');
    }

    hideAllMenus();
}

function onIconRightClick(e) {
    e.preventDefault();
    if (selectedIcon && selectedIcon !== this) {
        selectedIcon.classList.remove('selected');
    }
    selectedIcon = this;
    selectedIcon.classList.add('selected');
    showItemMenu(e.clientX, e.clientY);
}

function initIconsEvents() {
    const icons = document.querySelectorAll('.icon');
    icons.forEach(icon => {
        icon.addEventListener('click', onIconLeftClick);
        icon.addEventListener('contextmenu', onIconRightClick);
        // Для секретного файла: двойной клик
        icon.addEventListener('dblclick', function(e) {
            if (this.dataset.name === "Initiative.txt") {
                handleSecretFileClick();
            }
        });
    });
}

// Функция создания нового элемента (Grid/Flex размещает ярлыки)
function createItem(type) {
    let iconURL = '';
    let label = '';

    switch (type) {
        case 'folder':
            folderCount++;
            iconURL = "https://cdn-icons-png.flaticon.com/512/376/376998.png";
            label = `Новая папка (${folderCount})`;
            break;
        case 'textfile':
            fileCount++;
            iconURL = "https://cdn-icons-png.flaticon.com/512/337/337946.png";
            label = `Новый текстовый файл (${fileCount})`;
            break;
        case 'libre-draw':
            libreDrawCount++;
            iconURL = "https://cdn-icons-png.flaticon.com/512/185/185851.png";
            label = `Новый рисунок (${libreDrawCount})`;
            break;
        case 'libre-present':
            librePresentCount++;
            iconURL = "https://cdn-icons-png.flaticon.com/512/732/732030.png";
            label = `Новая презентация (${librePresentCount})`;
            break;
        case 'libre-sheet':
            libreSheetCount++;
            iconURL = "https://cdn-icons-png.flaticon.com/512/732/732017.png";
            label = `Новая таблица (${libreSheetCount})`;
            break;
        case 'libre-doc':
            libreDocCount++;
            iconURL = "https://cdn-icons-png.flaticon.com/512/732/732012.png";
            label = `Новый документ (${libreDocCount})`;
            break;
        default:
            return;
    }

    const iconDiv = document.createElement('div');
    iconDiv.className = 'icon';
    iconDiv.setAttribute('data-name', label);
    iconDiv.title = label;  // Показываем нативную подсказку при наведении

    const img = document.createElement('img');
    img.src = iconURL;

    const span = document.createElement('span');
    span.textContent = label;

    iconDiv.appendChild(img);
    iconDiv.appendChild(span);
    desktop.appendChild(iconDiv);

    iconDiv.addEventListener('click', onIconLeftClick);
    iconDiv.addEventListener('contextmenu', onIconRightClick);

    console.log("New item created:", label);

    hideAllMenus();
}

/* ========== ДЕЙСТВИЯ С ПРЕДМЕТОМ: ПЕРЕИМЕНОВАНИЕ И УДАЛЕНИЕ ========== */
function renameItem() {
    if (!selectedIcon) return;
    const oldName = selectedIcon.getAttribute('data-name') || 'Безымянный';
    showDialog({
        title: 'Переименовать',
        message: `Новое имя для «${oldName}»`,
        type: 'prompt',
        defaultValue: oldName,
        onConfirm: (newVal) => {
            if (newVal && newVal.trim() !== '') {
                selectedIcon.setAttribute('data-name', newVal.trim());
                selectedIcon.querySelector('span').textContent = newVal.trim();
            }
        }
    });
    hideAllMenus();
}

function deleteItem() {
    if (!selectedIcon) return;
    const name = selectedIcon.getAttribute('data-name') || 'Безымянный';
    showDialog({
        title: 'Удаление',
        message: `Удалить «${name}»?`,
        type: 'delete',
        onConfirm: () => {
            desktop.removeChild(selectedIcon);
            selectedIcon = null;
        }
    });
    hideAllMenus();
}

function isFolder(iconEl) {
    const img = iconEl.querySelector('img');
    if (!img) return false;
    return img.src.includes("376/376998") || img.src.includes("folder");
}

/* ========== КАСТОМНЫЕ ДИАЛОГИ ========== */
function showDialog({ title, message, type, defaultValue = '', onConfirm, onCancel }) {
    dialogTitle.textContent = title;
    dialogMessage.textContent = message;
    dialogInput.style.display = 'none';
    dialogInput.value = '';
    dialogButtons.innerHTML = '';

    if (type === 'prompt') {
        dialogInput.style.display = 'block';
        dialogInput.value = defaultValue;
        createButton('OK', 'ok-btn', () => {
            if (onConfirm) onConfirm(dialogInput.value);
            closeDialog();
        });
        createButton('Отмена', 'cancel-btn', () => {
            if (onCancel) onCancel();
            closeDialog();
        });
    } else if (type === 'delete') {
        createButton('Да', 'yes-btn', () => {
            if (onConfirm) onConfirm();
            closeDialog();
        });
        createButton('Нет', 'no-btn', () => {
            if (onCancel) onCancel();
            closeDialog();
        });
    } else {
        createButton('OK', 'ok-btn', () => {
            if (onConfirm) onConfirm();
            closeDialog();
        });
        createButton('Отмена', 'cancel-btn', () => {
            if (onCancel) onCancel();
            closeDialog();
        });
    }
    dialogOverlay.style.display = 'flex';
}

function createButton(text, className, onClick) {
    const btn = document.createElement('button');
    btn.textContent = text;
    btn.className = className;
    btn.addEventListener('click', onClick);
    dialogButtons.appendChild(btn);
}

function closeDialog() {
    dialogOverlay.style.display = 'none';
}

/* ========== ИНИЦИАЛИЗАЦИЯ ПАНЕЛИ НАГРАД ========== */
function initAwards() {
    console.log("Initializing awards...");
    const awards = document.querySelectorAll('.award');
    if (awards.length === 0) {
        console.error("No awards found!");
        return;
    }

    awards.forEach(award => {
        award.style.pointerEvents = 'auto';
        award.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log("Award clicked:", this.dataset.award);
            const awardName = this.dataset.award;
            const instruction = rewardInstructions[awardName] || "Инструкции для этой награды пока не заданы.";

            // Если выбрана награда первой этапа, показываем секретный файл
            if (awardName === "Бейджик Инициации") {
                const secretFile = document.querySelector('.secret-file');
                if (secretFile) {
                    const desktopRect = desktop.getBoundingClientRect();
                    const maxX = desktopRect.width - 100;
                    const maxY = desktopRect.height - 100;
                    const randomX = Math.floor(Math.random() * maxX);
                    const randomY = Math.floor(Math.random() * maxY);
                    secretFile.style.display = 'block';
                    secretFile.style.left = `${randomX}px`;
                    secretFile.style.top = `${randomY}px`;
                    secretFile.style.opacity = '0.2';
                    secretFile.removeEventListener('dblclick', handleSecretFileClick);
                    secretFile.addEventListener('dblclick', handleSecretFileClick);
                    console.log('Secret file position:', randomX, randomY);
                }
            }
            // Если выбрана награда второй этапа, активируем условие для терминала
            else if (awardName === "Токен Командной Строки") {
                localStorage.setItem("terminalTokenActive", "true");
            }
            showAssistant(instruction);
        });
    });
}

// Функция показа помощника
function showAssistant(message) {
    assistantText.textContent = message;
    assistantOverlay.style.display = 'flex';
}

// Функция закрытия помощника
function closeAssistant() {
    assistantOverlay.style.display = 'none';
}

/* ========== ОБРАБОТКА СЕКРЕТНОГО ФАЙЛА ========== */
function handleSecretFileClick() {
    showDialog({
        title: "Секретный файл",
        message: "Введите год создания Astra Linux:",
        type: 'prompt',
        defaultValue: '',
        onConfirm: (inputYear) => {
            const award = document.querySelector('[data-award="Бейджик Инициации"]');
            if (inputYear === '2008') {
                award.classList.add('correct');
                award.classList.remove('incorrect');
                showAssistant("Правильно! Astra Linux создана в 2008 году!");
            } else {
                award.classList.add('incorrect');
                award.classList.remove('correct');
                showAssistant("Неверно! Попробуйте ещё раз!");
            }
        }
    });
}

// Обработчик клавиш для вызова терминала (Alt+T)
document.addEventListener('keydown', function(e) {
    if (e.altKey && e.key.toLowerCase() === 't') {
        e.preventDefault();
        openTerminal();
    }
});

// Функция открытия терминала (переход на страницу терминала)
function openTerminal() {
    window.location.href = terminalUrl;
}
