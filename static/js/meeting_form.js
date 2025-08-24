document.addEventListener('DOMContentLoaded', function () {
  window.nextStep = function (current) {
    document.getElementById(`step${current}`).classList.add('d-none');
    document.getElementById(`step${current + 1}`).classList.remove('d-none');
  };

  window.prevStep = function (current) {
    document.getElementById(`step${current}`).classList.add('d-none');
    document.getElementById(`step${current - 1}`).classList.remove('d-none');
  };

  const addAgendaBtn = document.getElementById('addAgendaBtn');
	if (addAgendaBtn) {
	addAgendaBtn.addEventListener('click', function () {
		const container = document.getElementById('agendaContainer');
		const totalForms = document.getElementById('id_agendaitems-TOTAL_FORMS');
		const formCount = parseInt(totalForms.value);

		const template = document.querySelector('#agendaTemplate .agenda-item');
		const newForm = template.cloneNode(true);

		newForm.querySelectorAll('input, textarea, select').forEach(input => {
		const name = input.getAttribute('name');
		const id = input.getAttribute('id');
		if (name) input.setAttribute('name', name.replace('__prefix__', formCount));
		if (id) input.setAttribute('id', id.replace('__prefix__', formCount));
		input.value = '';
		});

		container.appendChild(newForm);
		totalForms.value = formCount + 1;
	});
  }

  const userSearch = document.getElementById('userSearch');
  if (userSearch) {
    userSearch.addEventListener('input', function () {
      const term = this.value.toLowerCase();
      const items = document.querySelectorAll('#userList .form-check');
      items.forEach(item => {
        const label = item.querySelector('label').textContent.toLowerCase();
        item.style.display = label.includes(term) ? 'block' : 'none';
      });
    });
  }
});
