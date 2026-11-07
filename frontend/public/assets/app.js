"use strict";
const translations = {
    ru: {
        adminConsole: "ADMIN CONSOLE",
        loginHero: "Профили — под контролем.",
        loginHeroDescription: "Безопасное управление профилями пользователей в одном месте.",
        adminOnly: "Доступ только для администраторов",
        adminConsoleRu: "АДМИНИСТРАТИВНАЯ ПАНЕЛЬ",
        welcomeBack: "С возвращением",
        loginPrompt: "Войдите с учётной записью администратора.",
        email: "Email",
        password: "Пароль",
        adminEmailPlaceholder: "admin@example.com",
        passwordPlaceholder: "Введите пароль",
        signIn: "Войти в систему",
        secureConnection: "Соединение защищено. Не передавайте свои данные другим лицам.",
        administrator: "Администратор",
        language: "Язык",
        signOut: "Выйти",
        management: "УПРАВЛЕНИЕ",
        profilesTitle: "Профили пользователей",
        profilesDescription: "Создавайте и обновляйте профили в рамках ваших полномочий.",
        newProfile: "Новый профиль",
        personalization: "ПЕРСОНАЛИЗАЦИЯ",
        sceneTitle: "Живой фон и музыка",
        motion: "Анимация",
        background: "Фон",
        city: "Мегаполис",
        nature: "Природа",
        ocean: "Океан",
        beach: "Пляж",
        anime: "Аниме-вдохновение",
        mediaSource: "Источник медиа",
        apiSource: "Защищённый API",
        localSource: "Локальный файл",
        backgroundFile: "Своя картинка",
        musicFile: "Фоновая музыка",
        mediaPrivacy: "Локальные файлы остаются в браузере и не загружаются на сервер. API-каталог доступен только после входа.",
        chooseLocalBackground: "Выберите локальный файл изображения.",
        chooseLocalMusic: "Выберите локальный аудиофайл.",
        localFileTooLarge: "Файл превышает лимит 15 МБ.",
        unsupportedMediaType: "Формат файла не поддерживается.",
        catalogUnavailable: "Каталог API временно недоступен. Используется анимированный фон.",
        noApiMusic: "В API-каталоге пока нет музыкальных файлов.",
        apiBackgroundApplied: "Фон загружен из защищённого API.",
        apiMusicReady: "Музыка загружена. Нажмите Play для воспроизведения.",
        localBackgroundApplied: "Локальный файл установлен как фон.",
        localMusicReady: "Локальная музыка готова. Нажмите Play для воспроизведения.",
        allProfiles: "Все профили",
        searchProfiles: "Поиск по профилям на текущей странице",
        searchPlaceholder: "Поиск на странице",
        loading: "Загрузка списка…",
        profilesOnPage: "профилей на этой странице",
        matchesOnPage: "из",
        onThisPage: "на этой странице",
        emptyProfiles: "Профилей пока нет",
        emptyProfilesDescription: "Создайте первый профиль, чтобы он появился в списке.",
        noSearchResults: "Ничего не найдено",
        changeSearch: "Измените поисковый запрос и попробуйте ещё раз.",
        createProfile: "Создать профиль",
        userColumn: "ПОЛЬЗОВАТЕЛЬ",
        statusColumn: "СТАТУС",
        createdColumn: "СОЗДАН",
        active: "Активен",
        inactive: "Неактивен",
        edit: "Изменить",
        deactivate: "Деактивировать",
        activate: "Активировать",
        delete: "Удалить",
        previous: "← Назад",
        next: "Далее →",
        page: "Страница",
        profilePrivacy: "Создание профиля не создаёт учётные данные или права входа.",
        profile: "ПРОФИЛЬ",
        editProfile: "Редактировать профиль",
        fullName: "Полное имя",
        close: "Закрыть",
        cancel: "Отмена",
        saveProfile: "Сохранить профиль",
        saveChanges: "Сохранить изменения",
        deleteConfirm: "Удалить профиль",
        cannotUndo: "Это действие нельзя отменить.",
        activateConfirm: "Вы уверены, что хотите активировать профиль",
        deactivateConfirm: "Вы уверены, что хотите деактивировать профиль",
        profileCreated: "Профиль создан.",
        profileSaved: "Изменения профиля сохранены.",
        profileDeleted: "Профиль удалён.",
        profileActivated: "Профиль активирован.",
        profileDeactivated: "Профиль деактивирован.",
        sessionExpired: "Сессия завершена. Войдите снова.",
        retryLogin: "Не удалось выполнить вход.",
        loadFailed: "Не удалось загрузить профили.",
        saveFailed: "Не удалось сохранить профиль.",
        statusFailed: "Не удалось изменить статус.",
        deleteFailed: "Не удалось удалить профиль.",
        logoutFailed: "Не удалось подтвердить отзыв сессии. Серверная сессия может действовать до истечения срока.",
        listUnavailable: "Список временно недоступен",
        resultsCount: "результатов",
        invalidRequest: "Ошибка запроса",
    },
    en: {
        adminConsole: "ADMIN CONSOLE",
        loginHero: "Profiles, under control.",
        loginHeroDescription: "Securely manage user profiles from one place.",
        adminOnly: "Administrator access only",
        adminConsoleRu: "ADMINISTRATOR CONSOLE",
        welcomeBack: "Welcome back",
        loginPrompt: "Sign in with your administrator account.",
        email: "Email",
        password: "Password",
        adminEmailPlaceholder: "admin@example.com",
        passwordPlaceholder: "Enter your password",
        signIn: "Sign in",
        secureConnection: "Your connection is secure. Never share your credentials.",
        administrator: "Administrator",
        language: "Language",
        signOut: "Sign out",
        management: "MANAGEMENT",
        profilesTitle: "User profiles",
        profilesDescription: "Create and update profiles within your permissions.",
        newProfile: "New profile",
        personalization: "PERSONALIZATION",
        sceneTitle: "Live background and music",
        motion: "Motion",
        background: "Background",
        city: "City",
        nature: "Nature",
        ocean: "Ocean",
        beach: "Beach",
        anime: "Anime-inspired",
        mediaSource: "Media source",
        apiSource: "Secure API",
        localSource: "Local file",
        backgroundFile: "Custom image",
        musicFile: "Background music",
        mediaPrivacy: "Local files stay in your browser and are never uploaded. The API catalog is available after sign-in.",
        chooseLocalBackground: "Choose a local image file.",
        chooseLocalMusic: "Choose a local audio file.",
        localFileTooLarge: "The file exceeds the 15 MB limit.",
        unsupportedMediaType: "This file format is not supported.",
        catalogUnavailable: "The API catalog is temporarily unavailable. The animated background remains active.",
        noApiMusic: "There are no music files in the API catalog yet.",
        apiBackgroundApplied: "Background loaded from the secure API.",
        apiMusicReady: "Music loaded. Press Play to start playback.",
        localBackgroundApplied: "Local file set as the background.",
        localMusicReady: "Local music is ready. Press Play to start playback.",
        allProfiles: "All profiles",
        searchProfiles: "Search profiles on the current page",
        searchPlaceholder: "Search this page",
        loading: "Loading profiles…",
        profilesOnPage: "profiles on this page",
        matchesOnPage: "of",
        onThisPage: "on this page",
        emptyProfiles: "No profiles yet",
        emptyProfilesDescription: "Create the first profile to see it here.",
        noSearchResults: "No results found",
        changeSearch: "Change your search and try again.",
        createProfile: "Create profile",
        userColumn: "USER",
        statusColumn: "STATUS",
        createdColumn: "CREATED",
        active: "Active",
        inactive: "Inactive",
        edit: "Edit",
        deactivate: "Deactivate",
        activate: "Activate",
        delete: "Delete",
        previous: "← Previous",
        next: "Next →",
        page: "Page",
        profilePrivacy: "Creating a profile does not create login credentials or grant access.",
        profile: "PROFILE",
        editProfile: "Edit profile",
        fullName: "Full name",
        close: "Close",
        cancel: "Cancel",
        saveProfile: "Save profile",
        saveChanges: "Save changes",
        deleteConfirm: "Delete profile",
        cannotUndo: "This action cannot be undone.",
        activateConfirm: "Are you sure you want to activate the profile",
        deactivateConfirm: "Are you sure you want to deactivate the profile",
        profileCreated: "Profile created.",
        profileSaved: "Profile changes saved.",
        profileDeleted: "Profile deleted.",
        profileActivated: "Profile activated.",
        profileDeactivated: "Profile deactivated.",
        sessionExpired: "Your session has expired. Please sign in again.",
        retryLogin: "Sign-in failed.",
        loadFailed: "Could not load profiles.",
        saveFailed: "Could not save the profile.",
        statusFailed: "Could not update the status.",
        deleteFailed: "Could not delete the profile.",
        logoutFailed: "Session revocation could not be confirmed. The server session may remain active until it expires.",
        listUnavailable: "The profile list is temporarily unavailable",
        resultsCount: "results",
        invalidRequest: "Request failed",
    },
};
const allowedMediaTypes = new Set([
    "image/jpeg",
    "image/png",
    "image/webp",
    "audio/mpeg",
    "audio/ogg",
    "audio/wav",
]);
const pageSize = 25;
let accessToken = null;
let tokenExpiresAt = 0;
let language = "ru";
let currentAdmin = null;
let currentPage = 0;
let users = [];
let editingUserId = null;
let toastTimer = 0;
let mediaCatalog = [];
let localBackgroundUrl = null;
let apiBackgroundUrl = null;
let localMusicUrl = null;
let apiMusicUrl = null;
function element(id) {
    const found = document.getElementById(id);
    if (!found) {
        throw new Error(`Missing required page element: ${id}`);
    }
    return found;
}
function t(key) {
    return translations[language][key];
}
function isMediaItem(value) {
    if (typeof value !== "object" || value === null) {
        return false;
    }
    const item = value;
    const categories = item.kind === "background" ? ["city", "nature", "ocean", "beach", "anime"] : ["ambient"];
    return (typeof item.id === "string" &&
        /^[a-f0-9]{32}$/.test(item.id) &&
        typeof item.url === "string" &&
        item.url === `/media/${item.id}` &&
        (item.kind === "background" || item.kind === "music") &&
        categories.includes(item.category ?? "") &&
        typeof item.title === "string" &&
        typeof item.content_type === "string" &&
        allowedMediaTypes.has(item.content_type) &&
        (item.kind === "background"
            ? item.content_type.startsWith("image/")
            : item.content_type.startsWith("audio/")));
}
function revokeUrl(url) {
    if (url?.startsWith("blob:")) {
        URL.revokeObjectURL(url);
    }
}
function resetMedia() {
    revokeUrl(localBackgroundUrl);
    revokeUrl(apiBackgroundUrl);
    revokeUrl(localMusicUrl);
    revokeUrl(apiMusicUrl);
    localBackgroundUrl = null;
    apiBackgroundUrl = null;
    localMusicUrl = null;
    apiMusicUrl = null;
    mediaCatalog = [];
    element("media-source").value = "api";
    element("background-category").value = "city";
    element("background-file").value = "";
    element("music-file").value = "";
    syncMediaSourceControls();
    const sceneImage = element("scene-image");
    sceneImage.removeAttribute("src");
    setHidden(sceneImage, true);
    const audio = element("background-audio");
    audio.pause();
    audio.removeAttribute("src");
    audio.load();
}
function applyLanguage() {
    document.documentElement.lang = language;
    document.title = `User Service — ${language === "ru" ? "профили" : "profiles"}`;
    document.querySelectorAll("[data-i18n]").forEach((node) => {
        const key = node.dataset.i18n;
        if (key && key in translations[language]) {
            node.textContent = t(key);
        }
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
        const key = node.dataset.i18nPlaceholder;
        if (key) {
            node.placeholder = t(key);
        }
    });
    document.querySelectorAll("[data-i18n-aria-label]").forEach((node) => {
        const key = node.dataset.i18nAriaLabel;
        if (key) {
            node.setAttribute("aria-label", t(key));
        }
    });
    element("language-select").value = language;
    element("login-language-select").value = language;
    renderUsers();
}
function setLanguage(value) {
    if (value !== "ru" && value !== "en") {
        return;
    }
    language = value;
    window.localStorage.setItem("user-service-language", language);
    applyLanguage();
}
function setHidden(target, hidden) {
    target.hidden = hidden;
}
function showMessage(target, message) {
    target.textContent = message;
    setHidden(target, false);
}
function clearMessage(target) {
    target.textContent = "";
    setHidden(target, true);
}
function messageFromBody(body, fallback) {
    if (typeof body?.detail === "string") {
        return body.detail;
    }
    if (Array.isArray(body?.detail)) {
        return body.detail.map((item) => item.msg).filter(Boolean).join("; ") || fallback;
    }
    return fallback;
}
async function request(path, init = {}) {
    const headers = new Headers(init.headers);
    if (accessToken) {
        headers.set("Authorization", `Bearer ${accessToken}`);
    }
    if (init.body && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
    }
    const response = await fetch(path, { ...init, headers });
    if (response.status === 401 && accessToken) {
        clearSession();
        const dialog = element("profile-dialog");
        if (dialog.open) {
            closeProfileDialog();
        }
        showLogin();
        showMessage(element("login-error"), t("sessionExpired"));
        throw new Error(t("sessionExpired"));
    }
    if (!response.ok) {
        let body = null;
        try {
            body = (await response.json());
        }
        catch {
            body = null;
        }
        throw new Error(messageFromBody(body, `${t("invalidRequest")} (${response.status})`));
    }
    if (response.status === 204) {
        return undefined;
    }
    return (await response.json());
}
function clearSession() {
    resetMedia();
    accessToken = null;
    tokenExpiresAt = 0;
    currentAdmin = null;
}
function showLogin() {
    setHidden(element("login-view"), false);
    setHidden(element("dashboard-view"), true);
    element("login-form").reset();
}
function showDashboard() {
    if (!currentAdmin) {
        return;
    }
    element("admin-email").textContent = currentAdmin.email;
    setHidden(element("login-view"), true);
    setHidden(element("dashboard-view"), false);
}
function initials(name) {
    const locale = language === "ru" ? "ru-RU" : "en-US";
    return name
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map((part) => part.charAt(0))
        .join("")
        .toLocaleUpperCase(locale) || "?";
}
function formattedDate(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
        return "—";
    }
    return new Intl.DateTimeFormat(language === "ru" ? "ru-RU" : "en-US", {
        day: "numeric",
        month: "short",
        year: "numeric",
    }).format(date);
}
function makeActionButton(label, className, action) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.textContent = label;
    button.addEventListener("click", action);
    return button;
}
function renderUsers() {
    const body = element("user-rows");
    const locale = language === "ru" ? "ru-RU" : "en-US";
    const search = element("search-input").value.trim().toLocaleLowerCase(locale);
    const visibleUsers = users.filter((user) => `${user.full_name} ${user.email}`.toLocaleLowerCase(locale).includes(search));
    body.replaceChildren();
    for (const user of visibleUsers) {
        const row = document.createElement("tr");
        const identityCell = document.createElement("td");
        const identity = document.createElement("div");
        const avatar = document.createElement("span");
        const details = document.createElement("div");
        const name = document.createElement("div");
        const email = document.createElement("div");
        identity.className = "user-cell";
        avatar.className = "avatar";
        avatar.setAttribute("aria-hidden", "true");
        avatar.textContent = initials(user.full_name);
        name.className = "user-name";
        name.textContent = user.full_name;
        email.className = "user-email";
        email.textContent = user.email;
        details.append(name, email);
        identity.append(avatar, details);
        identityCell.append(identity);
        const statusCell = document.createElement("td");
        const status = document.createElement("span");
        status.className = user.is_active ? "status" : "status status-inactive";
        status.textContent = user.is_active ? t("active") : t("inactive");
        statusCell.append(status);
        const dateCell = document.createElement("td");
        dateCell.className = "date-cell";
        dateCell.textContent = formattedDate(user.created_at);
        const actionsCell = document.createElement("td");
        const actions = document.createElement("div");
        actions.className = "row-actions";
        actions.append(makeActionButton(t("edit"), "text-button", () => openProfileDialog(user)), makeActionButton(user.is_active ? t("deactivate") : t("activate"), "text-button", () => void toggleUserStatus(user)), makeActionButton(t("delete"), "text-button text-button-danger", () => void deleteUser(user)));
        actionsCell.append(actions);
        row.append(identityCell, statusCell, dateCell, actionsCell);
        body.append(row);
    }
    const isEmpty = users.length === 0;
    const noMatches = !isEmpty && visibleUsers.length === 0;
    setHidden(element("empty-state"), !isEmpty && !noMatches);
    setHidden(element("table-wrap"), isEmpty || noMatches);
    element("empty-state-title").textContent = isEmpty ? t("emptyProfiles") : t("noSearchResults");
    element("empty-state-text").textContent = isEmpty
        ? t("emptyProfilesDescription")
        : t("changeSearch");
    setHidden(element("empty-create-button"), !isEmpty);
    element("result-count").textContent = search
        ? `${visibleUsers.length} ${t("matchesOnPage")} ${users.length} ${t("onThisPage")}`
        : `${users.length} ${t("profilesOnPage")}`;
    element("page-label").textContent = `${t("page")} ${currentPage + 1}`;
    element("previous-page").disabled = currentPage === 0;
    element("next-page").disabled = users.length < pageSize;
}
async function loadUsers() {
    clearMessage(element("page-error"));
    element("result-count").textContent = t("loading");
    try {
        users = await request(`/users?offset=${currentPage * pageSize}&limit=${pageSize}`);
        renderUsers();
    }
    catch (error) {
        showMessage(element("page-error"), error instanceof Error ? error.message : t("loadFailed"));
        element("result-count").textContent = t("listUnavailable");
    }
}
function selectedSource() {
    return element("media-source").value === "local" ? "local" : "api";
}
function syncMediaSourceControls() {
    const isLocal = selectedSource() === "local";
    setHidden(element("background-file-control"), !isLocal);
    setHidden(element("music-file-control"), !isLocal);
}
function resetBackgroundScene() {
    revokeUrl(apiBackgroundUrl);
    apiBackgroundUrl = null;
    const scene = element("ambient-scene");
    scene.dataset.scene = element("background-category").value;
    const image = element("scene-image");
    image.removeAttribute("src");
    setHidden(image, true);
}
function showMediaStatus(message) {
    element("media-status").textContent = message;
}
async function downloadMedia(item) {
    if (!accessToken || item.url !== `/media/${item.id}`) {
        throw new Error(t("catalogUnavailable"));
    }
    const response = await fetch(item.url, {
        headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (response.status === 401) {
        clearSession();
        showLogin();
        showMessage(element("login-error"), t("sessionExpired"));
        throw new Error(t("sessionExpired"));
    }
    if (!response.ok) {
        throw new Error(`${t("invalidRequest")} (${response.status})`);
    }
    const contentType = response.headers.get("content-type")?.split(";", 1)[0].toLowerCase();
    if (!contentType || contentType !== item.content_type || !/^(image|audio)\//.test(contentType)) {
        throw new Error(t("unsupportedMediaType"));
    }
    const declaredSize = Number(response.headers.get("content-length"));
    if (Number.isFinite(declaredSize) && declaredSize > 15 * 1024 * 1024) {
        await response.body?.cancel();
        throw new Error(t("localFileTooLarge"));
    }
    const reader = response.body?.getReader();
    if (!reader) {
        throw new Error(t("catalogUnavailable"));
    }
    const chunks = [];
    let totalSize = 0;
    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        totalSize += value.byteLength;
        if (totalSize > 15 * 1024 * 1024) {
            await reader.cancel();
            throw new Error(t("localFileTooLarge"));
        }
        const chunk = new ArrayBuffer(value.byteLength);
        new Uint8Array(chunk).set(value);
        chunks.push(chunk);
    }
    return new Blob(chunks, { type: item.content_type });
}
async function loadMediaCatalog() {
    try {
        const response = await request("/media/catalog");
        if (!Array.isArray(response)) {
            throw new Error(t("catalogUnavailable"));
        }
        mediaCatalog = response.filter(isMediaItem);
        await applyBackground();
        await applyMusic();
    }
    catch {
        mediaCatalog = [];
        resetBackgroundScene();
        clearAudio();
        showMediaStatus(t("catalogUnavailable"));
    }
}
async function applyBackground() {
    resetBackgroundScene();
    if (selectedSource() === "local") {
        const url = localBackgroundUrl;
        if (url) {
            element("scene-image").src = url;
            setHidden(element("scene-image"), false);
        }
        return;
    }
    const category = element("background-category").value;
    const item = mediaCatalog.find((candidate) => candidate.kind === "background" && candidate.category === category);
    if (!item) {
        return;
    }
    try {
        const blob = await downloadMedia(item);
        revokeUrl(apiBackgroundUrl);
        apiBackgroundUrl = URL.createObjectURL(blob);
        element("scene-image").src = apiBackgroundUrl;
        setHidden(element("scene-image"), false);
        showMediaStatus(t("apiBackgroundApplied"));
    }
    catch (error) {
        resetBackgroundScene();
        showMediaStatus(error instanceof Error ? error.message : t("catalogUnavailable"));
    }
}
function clearAudio() {
    const audio = element("background-audio");
    audio.pause();
    audio.removeAttribute("src");
    audio.load();
    revokeUrl(apiMusicUrl);
    apiMusicUrl = null;
}
async function applyMusic() {
    if (selectedSource() === "local") {
        clearAudio();
        if (localMusicUrl) {
            const audio = element("background-audio");
            audio.src = localMusicUrl;
            audio.load();
            showMediaStatus(t("localMusicReady"));
        }
        else {
            showMediaStatus(t("chooseLocalMusic"));
        }
        return;
    }
    clearAudio();
    const item = mediaCatalog.find((candidate) => candidate.kind === "music");
    if (!item) {
        showMediaStatus(t("noApiMusic"));
        return;
    }
    try {
        const blob = await downloadMedia(item);
        apiMusicUrl = URL.createObjectURL(blob);
        const audio = element("background-audio");
        audio.src = apiMusicUrl;
        audio.load();
        showMediaStatus(t("apiMusicReady"));
    }
    catch (error) {
        showMediaStatus(error instanceof Error ? error.message : t("catalogUnavailable"));
    }
}
function validateLocalFile(file, mediaType) {
    const allowedTypes = mediaType === "image"
        ? ["image/jpeg", "image/png", "image/webp"]
        : ["audio/mpeg", "audio/ogg", "audio/wav"];
    if (!allowedTypes.includes(file.type)) {
        notify(t("unsupportedMediaType"), true);
        return false;
    }
    if (file.size > 15 * 1024 * 1024) {
        notify(t("localFileTooLarge"), true);
        return false;
    }
    return true;
}
function useLocalBackground(file) {
    if (!validateLocalFile(file, "image")) {
        return;
    }
    revokeUrl(localBackgroundUrl);
    localBackgroundUrl = URL.createObjectURL(file);
    element("media-source").value = "local";
    syncMediaSourceControls();
    void Promise.all([applyBackground(), applyMusic()]);
    showMediaStatus(t("localBackgroundApplied"));
}
function useLocalMusic(file) {
    if (!validateLocalFile(file, "audio")) {
        return;
    }
    revokeUrl(localMusicUrl);
    localMusicUrl = URL.createObjectURL(file);
    element("media-source").value = "local";
    syncMediaSourceControls();
    void Promise.all([applyBackground(), applyMusic()]);
}
function openProfileDialog(user = null) {
    editingUserId = user?.id ?? null;
    element("dialog-title").textContent = user ? t("editProfile") : t("newProfile");
    element("profile-submit").textContent = user ? t("saveChanges") : t("createProfile");
    element("profile-name").value = user?.full_name ?? "";
    element("profile-email").value = user?.email ?? "";
    clearMessage(element("dialog-error"));
    element("profile-dialog").showModal();
    element("profile-name").focus();
}
function closeProfileDialog() {
    element("profile-dialog").close();
    element("profile-form").reset();
    editingUserId = null;
}
async function saveProfile(event) {
    event.preventDefault();
    const submit = element("profile-submit");
    const name = element("profile-name").value.trim();
    const email = element("profile-email").value.trim();
    const payload = { full_name: name, email };
    submit.disabled = true;
    clearMessage(element("dialog-error"));
    try {
        if (editingUserId) {
            await request(`/users/${encodeURIComponent(editingUserId)}`, {
                method: "PATCH",
                body: JSON.stringify(payload),
            });
            notify(t("profileSaved"));
        }
        else {
            await request("/users", {
                method: "POST",
                body: JSON.stringify(payload),
            });
            currentPage = 0;
            notify(t("profileCreated"));
        }
        closeProfileDialog();
        await loadUsers();
    }
    catch (error) {
        showMessage(element("dialog-error"), error instanceof Error ? error.message : t("saveFailed"));
    }
    finally {
        submit.disabled = false;
    }
}
async function toggleUserStatus(user) {
    const prompt = user.is_active ? t("deactivateConfirm") : t("activateConfirm");
    if (!window.confirm(`${prompt} «${user.full_name}»?`)) {
        return;
    }
    try {
        await request(`/users/${encodeURIComponent(user.id)}`, {
            method: "PATCH",
            body: JSON.stringify({ is_active: !user.is_active }),
        });
        notify(user.is_active ? t("profileDeactivated") : t("profileActivated"));
        await loadUsers();
    }
    catch (error) {
        notify(error instanceof Error ? error.message : t("statusFailed"), true);
    }
}
async function deleteUser(user) {
    if (!window.confirm(`${t("deleteConfirm")} «${user.full_name}»? ${t("cannotUndo")}`)) {
        return;
    }
    try {
        await request(`/users/${encodeURIComponent(user.id)}`, { method: "DELETE" });
        if (users.length === 1 && currentPage > 0) {
            currentPage -= 1;
        }
        notify(t("profileDeleted"));
        await loadUsers();
    }
    catch (error) {
        notify(error instanceof Error ? error.message : t("deleteFailed"), true);
    }
}
function notify(message, isError = false) {
    const toast = element("toast");
    toast.textContent = message;
    toast.classList.toggle("toast-error", isError);
    setHidden(toast, false);
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => setHidden(toast, true), 4200);
}
async function signIn(event) {
    event.preventDefault();
    const submit = element("login-submit");
    const error = element("login-error");
    submit.disabled = true;
    clearMessage(error);
    try {
        const credentials = {
            email: element("login-email").value.trim(),
            password: element("login-password").value,
        };
        const response = await request("/auth/login", {
            method: "POST",
            body: JSON.stringify(credentials),
        });
        accessToken = response.access_token;
        tokenExpiresAt = Date.now() + response.expires_in * 1000;
        element("login-form").reset();
        currentAdmin = await request("/auth/me");
        showDashboard();
        currentPage = 0;
        await Promise.all([loadUsers(), loadMediaCatalog()]);
    }
    catch (reason) {
        clearSession();
        showMessage(error, reason instanceof Error ? reason.message : t("retryLogin"));
    }
    finally {
        submit.disabled = false;
    }
}
async function signOut() {
    let revokeFailed = false;
    try {
        if (accessToken && Date.now() < tokenExpiresAt) {
            await request("/auth/logout", { method: "POST" });
        }
    }
    catch {
        revokeFailed = true;
    }
    finally {
        clearSession();
        showLogin();
    }
    if (revokeFailed) {
        notify(t("logoutFailed"), true);
    }
}
function setup() {
    const savedLanguage = window.localStorage.getItem("user-service-language");
    if (savedLanguage === "ru" || savedLanguage === "en") {
        language = savedLanguage;
    }
    applyLanguage();
    resetBackgroundScene();
    syncMediaSourceControls();
    element("login-form").addEventListener("submit", (event) => {
        void signIn(event);
    });
    element("profile-form").addEventListener("submit", (event) => {
        void saveProfile(event);
    });
    element("create-button").addEventListener("click", () => openProfileDialog());
    element("empty-create-button").addEventListener("click", () => openProfileDialog());
    element("dialog-close").addEventListener("click", closeProfileDialog);
    element("dialog-cancel").addEventListener("click", closeProfileDialog);
    element("logout-button").addEventListener("click", () => void signOut());
    element("language-select").addEventListener("change", (event) => {
        setLanguage(event.currentTarget.value);
    });
    element("login-language-select").addEventListener("change", (event) => {
        setLanguage(event.currentTarget.value);
    });
    element("media-source").addEventListener("change", () => {
        syncMediaSourceControls();
        void Promise.all([applyBackground(), applyMusic()]);
    });
    element("background-category").addEventListener("change", () => {
        void applyBackground();
    });
    element("background-file").addEventListener("change", (event) => {
        const file = event.currentTarget.files?.[0];
        if (file) {
            useLocalBackground(file);
        }
    });
    element("music-file").addEventListener("change", (event) => {
        const file = event.currentTarget.files?.[0];
        if (file) {
            useLocalMusic(file);
        }
    });
    element("motion-toggle").addEventListener("change", (event) => {
        document.body.classList.toggle("motion-off", !event.currentTarget.checked);
    });
    element("background-audio").addEventListener("error", () => {
        showMediaStatus(t("unsupportedMediaType"));
    });
    element("search-input").addEventListener("input", renderUsers);
    element("previous-page").addEventListener("click", () => {
        if (currentPage > 0) {
            currentPage -= 1;
            void loadUsers();
        }
    });
    element("next-page").addEventListener("click", () => {
        if (users.length === pageSize) {
            currentPage += 1;
            void loadUsers();
        }
    });
}
setup();
