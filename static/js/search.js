// Client‑side search using Lunr.js
class WorkspaceSearch {
  constructor() {
    this.index = null;
    this.documents = null;
    this.resultsContainer = document.getElementById('search-results');
    this.searchInput = document.getElementById('search-input');
    this.debounceTimer = null;
    this.init();
  }

  async init() {
    // Show loading spinner
    this.resultsContainer.innerHTML = `
      <div class="text-center p-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-emerald-600"></div>
        <p class="mt-2 text-gray-500">Loading search index…</p>
      </div>
    `;
    
    try {
      const response = await fetch('/search.json');
      const { index, documents } = await response.json();
      this.documents = documents;
      this.index = lunr.Index.load(index);
      console.log('🔍 Search index loaded:', this.documents.length, 'posts');
      
      // Hide results container, show hint
      this.resultsContainer.classList.add('hidden');
      this.showHint('Type at least 2 characters to search');
      this.setupSearch();
    } catch (error) {
      console.error('Failed to load search index:', error);
      this.resultsContainer.innerHTML = `
        <div class="text-center p-8 text-gray-500">
          <p>Search is temporarily unavailable.</p>
          <p class="text-sm mt-2">Browse the articles below instead.</p>
        </div>
      `;
    }
  }

  setupSearch() {
    this.searchInput.addEventListener('input', (e) => {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.search(e.target.value.trim());
      }, 300);
    });
    
    // Trigger search on Enter (if empty, maybe show recent?)
    this.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && this.searchInput.value.trim()) {
        e.preventDefault();
        clearTimeout(this.debounceTimer);
        this.search(this.searchInput.value.trim());
      }
    });
  }

  search(query) {
    if (!this.index || !this.documents) return;
    
    // Show results container
    this.resultsContainer.classList.remove('hidden');
    
    if (query.length < 2) {
      this.showHint('Type at least 2 characters to search');
      return;
    }

    let results;
    try {
      results = this.index.search(query);
    } catch (err) {
      console.warn('Search query failed:', err);
      this.showHint('Try a different search term');
      return;
    }

    if (results.length === 0) {
      this.showNoResults(query);
      return;
    }

    this.displayResults(results);
  }

  showHint(message) {
    this.resultsContainer.innerHTML = `
      <div class="text-center p-8 text-gray-500">
        <p>${message}</p>
      </div>
    `;
  }

  showNoResults(query) {
    this.resultsContainer.innerHTML = `
      <div class="text-center p-8">
        <p class="text-gray-700 font-medium">No results for <span class="text-primary">"${this.escapeHtml(query)}"</span></p>
        <p class="text-gray-500 text-sm mt-2">Try a different keyword or browse the categories.</p>
      </div>
    `;
  }

  displayResults(results) {
    const html = results.slice(0, 10).map(result => {
      const doc = this.documents.find(d => d.url === result.ref);
      if (!doc) return '';
      return `
        <a href="${doc.url}" class="block p-4 mb-3 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary transition-colors group">
          <div class="flex flex-col md:flex-row md:items-center gap-4">
            <div class="flex-1">
              <h4 class="font-display font-bold text-lg group-hover:text-primary transition-colors">${this.escapeHtml(doc.title)}</h4>
              ${doc.description ? `<p class="text-gray-600 dark:text-gray-400 text-sm mt-1">${this.escapeHtml(doc.description)}</p>` : ''}
              <div class="flex items-center gap-3 mt-3">
                ${doc.category ? `<span class="text-xs font-semibold px-2 py-1 rounded-full bg-primary/10 text-primary">${this.escapeHtml(doc.category)}</span>` : ''}
                <span class="text-gray-500 text-xs">${doc.date}</span>
              </div>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
            </svg>
          </div>
        </a>
      `;
    }).join('');
    
    this.resultsContainer.innerHTML = html;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize when DOM is ready
if (document.getElementById('search-overlay')) {
  document.addEventListener('DOMContentLoaded', () => {
    window.workspaceSearch = new WorkspaceSearch();
  });
}