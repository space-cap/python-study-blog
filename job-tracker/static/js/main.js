// Job Tracker Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize form handlers
    initializeUrlForm();
    initializeJobActions();
});

// URL 입력 폼 핸들러
function initializeUrlForm() {
    const urlForm = document.getElementById('url-form');
    if (!urlForm) return;

    urlForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const urlInput = document.getElementById('url-input');
        const submitBtn = document.getElementById('submit-btn');
        const originalBtnText = submitBtn.innerHTML;
        
        // 입력 검증
        const url = urlInput.value.trim();
        if (!url) {
            showAlert('URL을 입력해주세요.', 'warning');
            return;
        }

        if (!isValidUrl(url)) {
            showAlert('올바른 URL 형식을 입력해주세요.', 'warning');
            return;
        }

        // 로딩 상태 설정
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> 크롤링 시작 중...';

        try {
            const response = await fetch('/api/jobs/crawl', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            if (response.ok) {
                showAlert(data.message, 'success');
                urlInput.value = '';
                
                // 잠시 후 채용공고 페이지로 이동
                setTimeout(() => {
                    window.location.href = '/jobs';
                }, 2000);
            } else {
                throw new Error(data.detail || '크롤링 시작에 실패했습니다.');
            }
        } catch (error) {
            showAlert(error.message, 'danger');
        } finally {
            // 로딩 상태 해제
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
}

// 채용공고 관련 액션 핸들러
function initializeJobActions() {
    // 삭제 버튼 핸들러
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-job-btn')) {
            e.preventDefault();
            const jobId = e.target.dataset.jobId;
            const jobTitle = e.target.dataset.jobTitle;
            
            if (confirm(`"${jobTitle}" 채용공고를 삭제하시겠습니까?`)) {
                deleteJob(jobId);
            }
        }
    });

    // 새로고침 버튼 핸들러
    const refreshBtn = document.getElementById('refresh-jobs');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            window.location.reload();
        });
    }
}

// 채용공고 삭제
async function deleteJob(jobId) {
    try {
        const response = await fetch(`/api/jobs/${jobId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message, 'success');
            // 해당 행 제거
            const jobRow = document.querySelector(`[data-job-id="${jobId}"]`).closest('tr');
            if (jobRow) {
                jobRow.remove();
            }
        } else {
            throw new Error(data.detail || '삭제에 실패했습니다.');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// URL 유효성 검사
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// 알림 표시
function showAlert(message, type = 'info') {
    // 기존 알림 제거
    const existingAlert = document.querySelector('.alert-dismissible');
    if (existingAlert) {
        existingAlert.remove();
    }

    // 새 알림 생성
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // 컨테이너 찾아서 삽입
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }

    // 자동 제거 (5초 후)
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 페이지네이션 핸들러
function setupPagination() {
    const paginationLinks = document.querySelectorAll('.pagination .page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.href;
            if (url) {
                window.location.href = url;
            }
        });
    });
}

// 검색 기능
function setupSearch() {
    const searchInput = document.getElementById('job-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const jobItems = document.querySelectorAll('.job-item');

        jobItems.forEach(item => {
            const title = item.querySelector('.job-title').textContent.toLowerCase();
            const company = item.querySelector('.job-company').textContent.toLowerCase();
            const location = item.querySelector('.job-location').textContent.toLowerCase();

            const isVisible = title.includes(searchTerm) || 
                            company.includes(searchTerm) || 
                            location.includes(searchTerm);

            item.style.display = isVisible ? 'block' : 'none';
        });
    });
}

// 유틸리티 함수들
const utils = {
    // 날짜 포맷팅
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    // 텍스트 자르기
    truncateText: function(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    // 로딩 스피너 표시/숨김
    showLoading: function(element) {
        const originalContent = element.innerHTML;
        element.innerHTML = '<span class="loading"></span> 로딩 중...';
        element.disabled = true;
        return originalContent;
    },

    hideLoading: function(element, originalContent) {
        element.innerHTML = originalContent;
        element.disabled = false;
    }
};