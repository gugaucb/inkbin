// INK Editorial JavaScript Controller

function t(key, fallback = key, params = {}) {
  const dict = window.__INK_I18N__ || {};
  let val = dict[key] !== undefined ? dict[key] : fallback;
  if (params && typeof params === 'object') {
    for (const [k, v] of Object.entries(params)) {
      val = val.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
    }
  }
  return val;
}

document.addEventListener('DOMContentLoaded', () => {
  setupEditor();
  setupLocalHistory();
  setupViewerCopyActions();
});

function setupEditor() {
  const textarea = document.getElementById('paste-content');
  const form = document.getElementById('paste-form');
  const charCountEl = document.getElementById('char-count');
  const byteCountEl = document.getElementById('byte-count');
  const submitBtn = document.getElementById('submit-btn');

  if (!textarea) return;

  // Tab key indentation support
  textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const value = textarea.value;

      textarea.value = value.substring(0, start) + '    ' + value.substring(end);
      textarea.selectionStart = textarea.selectionEnd = start + 4;
      updateStats();
    }
  });

  function updateStats() {
    const text = textarea.value;
    const chars = text.length;
    const bytes = new Blob([text]).size;

    if (charCountEl) {
      const charsText = t('editor.chars', `${chars.toLocaleString()} caracteres`, { count: chars.toLocaleString() });
      charCountEl.innerHTML = `<i class="ti ti-letter-case icon-sm" aria-hidden="true"></i> <span>${charsText}</span>`;
    }
    if (byteCountEl) {
      const maxText = t('editor.bytes_max', 'máx');
      let byteStr = '';
      if (bytes < 1024) {
        byteStr = `${bytes} B`;
      } else if (bytes < 1024 * 1024) {
        byteStr = `${(bytes / 1024).toFixed(1)} KB`;
      } else {
        byteStr = `${(bytes / (1024 * 1024)).toFixed(2)} MB / 1 MB ${maxText}`;
      }
      byteCountEl.innerHTML = `<i class="ti ti-database icon-sm" aria-hidden="true"></i> <span>${byteStr}</span>`;
    }
  }

  textarea.addEventListener('input', updateStats);
  updateStats();

  // Async form submission
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const content = textarea.value;
      if (!content.trim()) {
        alert(t('editor.alert_empty', 'Por favor, insira o conteúdo do paste antes de publicar.'));
        return;
      }

      const title = document.getElementById('paste-title')?.value || null;
      const language = document.getElementById('paste-language')?.value || 'plaintext';
      const expiration = document.getElementById('paste-expiration')?.value || 'never';
      const password = document.getElementById('paste-password')?.value || null;

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="ti ti-loader animate-spin" aria-hidden="true"></i> <span>${t('editor.publishing_btn', 'Publicando...')}</span>`;
      }

      try {
        const response = await fetch('/api/pastes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title || null,
            content,
            language,
            expiration,
            password: password || null,
          }),
        });

        if (!response.ok) {
          const err = await response.json();
          alert(err.detail || t('editor.alert_error', 'Ocorreu um erro ao publicar o paste.'));
          return;
        }

        const data = await response.json();
        // Save to local history
        saveToLocalHistory({
          slug: data.slug,
          title: data.title || t('viewer.untitled', 'Sem título'),
          language: data.language,
          created_at: data.created_at,
          admin_delete_token: data.admin_delete_token,
          url: data.url,
        });

        // Show Success Modal
        showSuccessModal(data);
      } catch (err) {
        alert(t('editor.alert_network', 'Falha na conexão ao publicar o paste.'));
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<i class="ti ti-upload" aria-hidden="true"></i> <span>${t('editor.submit_btn', 'Publicar texto')}</span>`;
        }
      }
    });
  }
}

function showSuccessModal(data) {
  const modal = document.getElementById('success-modal');
  if (!modal) {
    window.location.href = data.url;
    return;
  }

  document.getElementById('modal-slug-url').value = data.url;
  document.getElementById('modal-delete-token').textContent = data.admin_delete_token;
  document.getElementById('modal-view-link').href = data.url;

  modal.style.display = 'flex';
}

function closeSuccessModal() {
  const modal = document.getElementById('success-modal');
  if (modal) {
    modal.style.display = 'none';
  }
}

function copyToClipboard(elementId, feedbackBtnId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.value || el.textContent;

  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById(feedbackBtnId);
    if (btn) {
      const originalHtml = btn.innerHTML;
      btn.innerHTML = `<i class="ti ti-check" aria-hidden="true"></i> <span>${t('modal.copied', 'Copiado!')}</span>`;
      setTimeout(() => {
        btn.innerHTML = originalHtml;
      }, 2000);
    }
  }).catch(() => {
    alert(t('clipboard.copy_failed', 'Não foi possível copiar. Selecione o texto e copie manualmente.'));
  });
}

function setupViewerCopyActions() {
  const copyCodeBtn = document.getElementById('copy-code-btn');
  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      const codeEl = document.getElementById('raw-code');
      if (!codeEl) return;
      navigator.clipboard.writeText(codeEl.textContent).then(() => {
        copyCodeBtn.innerHTML = `<i class="ti ti-check" aria-hidden="true"></i> <span>${t('viewer.code_copied', 'Código copiado!')}</span>`;
        setTimeout(() => {
          copyCodeBtn.innerHTML = `<i class="ti ti-copy" aria-hidden="true"></i> <span>${t('viewer.copy_code', 'Copiar código')}</span>`;
        }, 2000);
      });
    });
  }
}

function saveToLocalHistory(item) {
  try {
    const history = JSON.parse(localStorage.getItem('inkbin_history') || '[]');
    const filtered = history.filter(h => h.slug !== item.slug);
    filtered.unshift(item);
    const limited = filtered.slice(0, 15);
    localStorage.setItem('inkbin_history', JSON.stringify(limited));
    renderHistoryList(limited);
  } catch (e) {
    console.warn('LocalStorage error', e);
  }
}

function removePasteFromHistory(slug) {
  try {
    const history = JSON.parse(localStorage.getItem('inkbin_history') || '[]');
    const filtered = history.filter(h => h.slug !== slug);
    localStorage.setItem('inkbin_history', JSON.stringify(filtered));
    renderHistoryList(filtered);
  } catch (e) {
    console.warn('LocalStorage error', e);
  }
}

function clearLocalHistory() {
  const confirmMsg = t('nav.clear_history_confirm', 'Tem certeza de que deseja limpar todo o histórico local?');
  if (confirm(confirmMsg)) {
    try {
      localStorage.removeItem('inkbin_history');
      renderHistoryList([]);
    } catch (e) {
      console.warn('LocalStorage error', e);
    }
  }
}

function setupLocalHistory() {
  try {
    const history = JSON.parse(localStorage.getItem('inkbin_history') || '[]');
    renderHistoryList(history);

    const clearBtn = document.getElementById('clear-history-btn');
    if (clearBtn) {
      clearBtn.addEventListener('click', (e) => {
        e.preventDefault();
        clearLocalHistory();
      });
    }
  } catch (e) {
    // Ignore
  }
}

function renderHistoryList(items) {
  const container = document.getElementById('local-history-container');
  const clearBtn = document.getElementById('clear-history-btn');
  if (!container) return;

  if (!items || items.length === 0) {
    if (clearBtn) clearBtn.style.display = 'none';
    container.innerHTML = `<div style="font-size: 12px; color: var(--text-muted); padding: 8px;">${t('nav.no_history', 'Nenhum paste recente neste navegador.')}</div>`;
    return;
  }

  if (clearBtn) clearBtn.style.display = 'inline-flex';

  const deleteTitle = t('nav.delete_item_title', 'Remover do histórico');
  const deleteAria = t('nav.delete_item_aria', 'Remover este paste do histórico');

  container.innerHTML = items.map(item => `
    <div class="history-item-wrapper">
      <a href="/p/${item.slug}" class="history-item">
        <span class="history-title"><i class="ti ti-file-text icon-sm" aria-hidden="true"></i> <span>${escapeHtml(item.title || t('viewer.untitled', 'Sem título'))}</span></span>
        <span class="history-date">${item.language} · ${new Date(item.created_at).toLocaleDateString()}</span>
      </a>
      <button type="button" class="btn-delete-history-item" data-slug="${item.slug}" title="${deleteTitle}" aria-label="${deleteAria}">
        <i class="ti ti-x icon-sm" aria-hidden="true"></i>
      </button>
    </div>
  `).join('');

  container.querySelectorAll('.btn-delete-history-item').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      e.preventDefault();
      const slug = btn.getAttribute('data-slug');
      removePasteFromHistory(slug);
    });
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}
