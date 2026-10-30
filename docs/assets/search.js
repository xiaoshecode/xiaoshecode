const search = document.querySelector('#search');
const kind = document.querySelector('#kind');
const cards = [...document.querySelectorAll('.card')];
function filterRepositories() {
  const term = search.value.trim().toLowerCase();
  let count = 0;
  for (const card of cards) {
    const visible = card.dataset.search.includes(term)
      && (kind.value === 'all' || card.dataset.kind === kind.value);
    card.hidden = !visible;
    if (visible) count += 1;
  }
  document.querySelector('#count').textContent = `显示 ${count} 个仓库`;
}
search.addEventListener('input', filterRepositories);
kind.addEventListener('change', filterRepositories);
