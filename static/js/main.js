/**
 * Digital Notice Board System
 * Client-Side Interactivity, Live Clock, Modal Dialogs & Helpers
 */

document.addEventListener('DOMContentLoaded', () => {
    initLiveClock();
    initMobileNav();
    initFlashAutoDismiss();
    initKeyboardShortcuts();
});

/**
 * Updates the live header clock every second
 */
function initLiveClock() {
    const clockEl = document.getElementById('liveClock');
    if (!clockEl) return;

    function update() {
        const now = new Date();
        const options = {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        };
        clockEl.textContent = now.toLocaleDateString('en-US', options);
    }

    update();
    setInterval(update, 1000);
}

/**
 * Mobile Navigation Menu Hamburger Toggle
 */
function initMobileNav() {
    const toggleBtn = document.getElementById('navToggle');
    const mainNav = document.getElementById('mainNav');

    if (toggleBtn && mainNav) {
        toggleBtn.addEventListener('click', () => {
            mainNav.classList.toggle('open');
            toggleBtn.classList.toggle('active');
        });
    }
}

/**
 * Automatically dismiss flash notifications after 5 seconds
 */
function initFlashAutoDismiss() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (alert.parentElement) alert.remove();
            }, 400);
        }, 5000);
    });
}

/**
 * Global Keyboard Shortcuts (e.g. Esc to close modal)
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeNoticeModal();
        }
    });
}

/**
 * Opens notice modal by fetching JSON data from /api/notice/<id>
 */
async function openNoticeModal(noticeId) {
    const backdrop = document.getElementById('noticeModalBackdrop');
    if (!backdrop) return;

    // Loading state
    document.getElementById('modalTitle').textContent = 'Loading notice...';
    document.getElementById('modalContent').textContent = 'Please wait while notice details are retrieved.';
    document.getElementById('modalPostedBy').textContent = '...';
    document.getElementById('modalCreatedAt').textContent = '...';
    document.getElementById('modalExtraInfo').innerHTML = '';
    backdrop.classList.add('open');

    try {
        const response = await fetch(`/api/notice/${noticeId}`);
        if (!response.ok) throw new Error('Failed to load notice');
        const data = await response.json();

        if (data.success && data.notice) {
            const n = data.notice;
            document.getElementById('modalTitle').textContent = n.title;
            document.getElementById('modalContent').textContent = n.content;
            document.getElementById('modalPostedBy').textContent = n.posted_by;
            document.getElementById('modalCreatedAt').textContent = n.created_at;

            // Permanent detail link
            document.getElementById('modalPermLink').href = `/notice/${n.id}`;

            // Category badge
            const catBadge = document.getElementById('modalCategoryBadge');
            catBadge.textContent = n.category;
            catBadge.className = `badge badge-category cat-${n.category.toLowerCase()}`;

            // Priority badge
            const priBadge = document.getElementById('modalPriorityBadge');
            priBadge.textContent = n.priority;
            priBadge.className = `badge badge-priority badge-priority-${n.priority.toLowerCase()}`;
            if (n.priority === 'Urgent') {
                priBadge.innerHTML = '<span class="pulse-dot"></span> Urgent';
            }

            // Expiry info if present
            if (n.expiry_date) {
                document.getElementById('modalExtraInfo').innerHTML = `
                    <div class="card-expiry-badge">
                        <span>Notice valid until: <strong>${n.expiry_date}</strong></span>
                    </div>
                `;
            } else {
                document.getElementById('modalExtraInfo').innerHTML = '';
            }
        }
    } catch (err) {
        document.getElementById('modalTitle').textContent = 'Unable to Load Notice';
        document.getElementById('modalContent').textContent = 'An error occurred while fetching notice details. Please try again.';
    }
}

/**
 * Closes notice modal
 */
function closeNoticeModal(event) {
    const backdrop = document.getElementById('noticeModalBackdrop');
    if (!backdrop) return;

    if (!event || event.target === backdrop || event.target.classList.contains('modal-close-btn') || event.target.closest('.modal-close-btn') || event.target.tagName === 'BUTTON') {
        backdrop.classList.remove('open');
    }
}

/**
 * Prints current modal notice
 */
function printModalNotice() {
    const permLink = document.getElementById('modalPermLink').href;
    if (permLink && permLink !== '#') {
        window.open(permLink, '_blank');
    }
}

/**
 * Copies the current URL to clipboard with user feedback
 */
function copyCurrentUrl() {
    const btn = document.getElementById('copyLinkBtn');
    if (!btn) return;

    navigator.clipboard.writeText(window.location.href).then(() => {
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            <span>Link Copied!</span>
        `;
        btn.classList.add('btn-primary');
        btn.classList.remove('btn-secondary');

        setTimeout(() => {
            btn.innerHTML = originalHtml;
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-secondary');
        }, 2500);
    }).catch(() => {
        alert('Notice link copied: ' + window.location.href);
    });
}

