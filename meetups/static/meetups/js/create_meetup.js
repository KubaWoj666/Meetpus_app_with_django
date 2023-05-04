// const addLocationBtn = document.getElementById("add_location");
// const modal = document.getElementById("modal-body")

// addLocationBtn.addEventListener('click', () => {
//     console.log('You clicked the button');
//     modal.style.add= "show"
//   });



// Show Modal
// const openModalButton = document.getElementById("add_location");
// const modalWindowOverlay = document.getElementById("MyModal");

// const showModalWindow = () => {
//   modalWindowOverlay.style.display = 'flex';
// }
// openModalButton.addEventListener("click", showModalWindow);

// const myModal = document.getElementById('MyModal')
// const myInput = document.getElementById('add_location')

// myModal.addEventListener('shown.bs.modal', () => {
//   myInput.focus()
// })


// skrypt do obsługi formularza add location
// $(document).ready(function() {
//   var locationModal = $('#location-modal');
//   var locationForm = $('#location-form');
//   var locationSelect = $('#id_location');

//   // wyświetl modal z formularzem add location
//   $('#add-location-btn').click(function() {
//     locationModal.modal('show');
//   });

//   // zapisz nową lokację
//   locationForm.submit(function(event) {
//     event.preventDefault();
//     $.ajax({
//       url: '/locations/create/',
//       type: 'POST',
//       data: locationForm.serialize(),
//       success: function(response) {
//         // dodaj nową lokację do pola wyboru
//         var newOption = $('<option>', {
//           value: response.id,
//           text: response.name,
//         });
//         locationSelect.append(newOption);

//         // zamknij modal
//         locationModal.modal('hide');
//       },
//       error: function(response) {
//         console.log('Error:', response);
//       }
//     });
//   });
// });
