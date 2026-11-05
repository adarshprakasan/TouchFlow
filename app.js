const modeButtons = [...document.querySelectorAll('.mode-tab')];
const views = {
  trackpad: document.getElementById('trackpadView'),
  keyboard: document.getElementById('keyboardView'),
  gestures: document.getElementById('gesturesView'),
};
const surface = document.getElementById('touchSurface');
const surfacePointer = document.getElementById('surfacePointer');
const desktopCursor = document.getElementById('desktopCursor');
const toast = document.getElementById('surfaceToast');
const dialog = document.getElementById('infoDialog');
let toastTimer;

function showDialog(title, body, eyebrow = 'DEMO MODE') {
  document.getElementById('dialogTitle').textContent = title;
  document.getElementById('dialogBody').textContent = body;
  document.getElementById('dialogEyebrow').textContent = eyebrow;
  dialog.showModal();
}

modeButtons.forEach((button) => button.addEventListener('click', () => {
  modeButtons.forEach((item) => item.classList.toggle('active', item === button));
  Object.entries(views).forEach(([name, view]) => view.classList.toggle('active', name === button.dataset.mode));
}));

function setPointer(clientX, clientY) {
  const rect = surface.getBoundingClientRect();
  const x = Math.max(5, Math.min(95, ((clientX - rect.left) / rect.width) * 100));
  const y = Math.max(5, Math.min(95, ((clientY - rect.top) / rect.height) * 100));
  surfacePointer.style.left = `${x}%`;
  surfacePointer.style.top = `${y}%`;
  surfacePointer.style.opacity = '1';
  desktopCursor.style.left = `${Math.max(8, Math.min(92, x * 0.78 + 10))}%`;
  desktopCursor.style.top = `${Math.max(8, Math.min(90, y * 0.72 + 10))}%`;
  desktopCursor.classList.add('moved');
}
function showToast(message) {
  toast.textContent = message;
  toast.style.opacity = '1';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.style.opacity = '0'; }, 900);
}
surface.addEventListener('pointerdown', (event) => {
  surface.setPointerCapture(event.pointerId);
  setPointer(event.clientX, event.clientY);
});
surface.addEventListener('pointermove', (event) => {
  if (event.buttons || event.pointerType === 'touch') setPointer(event.clientX, event.clientY);
});
surface.addEventListener('pointerup', () => showToast('In-page pointer moved'));
surface.addEventListener('wheel', (event) => { event.preventDefault(); showToast(event.deltaY < 0 ? 'Scroll up preview' : 'Scroll down preview'); }, { passive: false });

function flashClick(kind) {
  showToast(`${kind} click preview`);
  document.querySelectorAll('.click-button').forEach((button) => button.classList.toggle('flash', button.id === (kind === 'Left' ? 'leftClick' : 'rightClick')));
  setTimeout(() => document.querySelectorAll('.click-button').forEach((button) => button.classList.remove('flash')), 220);
}
document.getElementById('leftClick').addEventListener('click', () => flashClick('Left'));
document.getElementById('rightClick').addEventListener('click', () => flashClick('Right'));
document.getElementById('demoAction').addEventListener('click', () => showDialog('Nice click', 'This button was activated inside the TouchFlow demo page. System-wide control will come with the desktop companion.'));

const sensitivity = document.getElementById('sensitivity');
const speedNames = ['Slow', 'Gentle', 'Medium', 'Fast', 'Very fast'];
sensitivity.addEventListener('input', () => { document.getElementById('speedValue').textContent = speedNames[Number(sensitivity.value) - 1]; });

const keyboardInput = document.getElementById('keyboardInput');
keyboardInput.addEventListener('input', () => {
  document.getElementById('typedPreview').textContent = keyboardInput.value || 'Your text will appear here.';
});
document.querySelectorAll('[data-key]').forEach((button) => button.addEventListener('click', () => {
  const key = button.dataset.key;
  if (key === 'Enter') keyboardInput.value += '\n';
  else if (key === 'Escape') keyboardInput.value = '';
  else keyboardInput.value += key;
  keyboardInput.dispatchEvent(new Event('input'));
  keyboardInput.focus();
}));

document.querySelectorAll('.gesture-card').forEach((card) => card.addEventListener('click', () => {
  document.getElementById('gesturePreview').textContent = `${card.querySelector('b').textContent} preview`;
}));
function pairingNotice() {
  showDialog('Desktop companion coming next', 'Pairing will be enabled when the standalone desktop companion is ready. For now, try the in-page pointer, keyboard preview, and gesture panel.', 'PAIRING');
}
document.getElementById('pairButton').addEventListener('click', pairingNotice);
document.getElementById('pairSmall').addEventListener('click', pairingNotice);
document.getElementById('privacyButton').addEventListener('click', () => showDialog('Private by design', 'This prototype sends no input anywhere. Your touch, text, and clicks stay in this browser page. Pairing and network permissions are not active yet.', 'PRIVACY & SAFETY'));
document.getElementById('closeDialog').addEventListener('click', () => dialog.close());
document.getElementById('dialogOk').addEventListener('click', () => dialog.close());
