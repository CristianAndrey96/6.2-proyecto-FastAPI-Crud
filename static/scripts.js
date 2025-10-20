let idEditar = null;
window.onload = function () {
  cargarCarros();
  document
    .getElementById("form-carro")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      const id = document.getElementById("id").value;
      const marca = document.getElementById("marca").value;
      const modelo = parseInt(document.getElementById("modelo").value);
      if (modoEditar) {
        // Modo actualización
        fetch(`/carros/${idEditar}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id, marca, modelo }),
        })
          .then((response) => {
            if (!response.ok) throw new Error("Error al actualizar");
            return response.json();
          })
          .then(() => {
            resetFormulario();
            cargarCarros();
          })
          .catch((error) => console.error("Error al actualizar:", error));
      } else {
        // Modo agregar
        fetch("/carros", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id, marca, modelo }),
        })
          .then((response) => {
            if (!response.ok) throw new Error("Error al agregar");
            return response.json();
          })
          .then(() => {
            document.getElementById("form-carro").reset();
            cargarCarros();
          })
          .catch((error) => console.error("Error al agregar:", error));
      }
    });
};
function cargarCarros() {
  fetch("/carros")
    .then((response) => response.json())
    .then((data) => {
      const lista = document.getElementById("lista-carros");
      lista.innerHTML = "";
      data.forEach((carro) => {
        const item = document.createElement("li");
        item.textContent = `ID: ${carro.id} - Marca: ${carro.marca} - Modelo:

${carro.modelo}`;

        // Botón eliminar
        const btnEliminar = document.createElement("button");
        btnEliminar.textContent = "Eliminar";
        btnEliminar.style.marginLeft = "10px";
        btnEliminar.onclick = () => eliminarCarro(carro.id);
        // Botón editar
        const btnEditar = document.createElement("button");
        btnEditar.textContent = "Editar";
        btnEditar.style.marginLeft = "5px";
        btnEditar.onclick = () => prepararEdicion(carro);
        item.appendChild(btnEliminar);
        item.appendChild(btnEditar);
        lista.appendChild(item);
      });
    })
    .catch((error) => console.error("Error al cargar carros:", error));
}
function eliminarCarro(id) {
  if (!confirm(`¿Eliminar carro con ID ${id}?`)) return;
  fetch(`/carros/${id}`, { method: "DELETE" })
    .then((response) => {
      if (!response.ok) throw new Error("Error al eliminar");
      cargarCarros();
    })
    .catch((error) => console.error("Error al eliminar carro:", error));
}
function prepararEdicion(carro) {
  document.getElementById("id").value = carro.id;
  document.getElementById("marca").value = carro.marca;
  document.getElementById("modelo").value = carro.modelo;
  modoEditar = true;
  idEditar = carro.id;
  // Cambiar botón
  document.querySelector('#form-carro button[type="submit"]').textContent =
    "Actualizar Carro";
}
function resetFormulario() {
  document.getElementById("form-carro").reset();
  modoEditar = false;
  idEditar = null;
  document.querySelector('#form-carro button[type="submit"]').textContent =
    "Agregar Carro";
}
