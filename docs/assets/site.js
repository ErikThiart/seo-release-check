const demoControls = document.querySelector('.release-tabs');
const demoButtons = Array.from(demoControls.querySelectorAll('button[data-release-panel]'));

for (const button of demoButtons) {
  button.addEventListener('click', () => {
    for (const peer of demoButtons) {
      const selected = peer === button;
      peer.setAttribute('aria-pressed', String(selected));
      document.getElementById(peer.dataset.releasePanel).hidden = !selected;
    }
  });
}
demoControls.hidden = false;

const copyButton = document.querySelector('.copy-button');
const command = document.getElementById('install-command');
const feedback = document.getElementById('copy-feedback');
let feedbackTimer;
let previousMessage = '';

async function copyCommand() {
  let message;
  try {
    await navigator.clipboard.writeText(command.textContent.trim());
    message = 'Copied';
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(command);
    selection.removeAllRanges();
    selection.addRange(range);
    message = 'Command selected. Copy it manually.';
  }

  if (message === previousMessage) message += '\u00A0';
  feedback.textContent = message;
  previousMessage = message;
  clearTimeout(feedbackTimer);
  feedbackTimer = setTimeout(() => { feedback.textContent = ''; }, 3500);
}

if ('CommandEvent' in window) {
  command.addEventListener('command', (event) => {
    if (event.command === '--copy') copyCommand();
  });
} else {
  copyButton.addEventListener('click', copyCommand);
}
copyButton.hidden = false;
