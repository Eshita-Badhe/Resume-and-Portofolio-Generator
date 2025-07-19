function downloadPDF() {
    fetch('/download_resume_pdf')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to download PDF.');
            }
            return response.blob();
        })
        .then(blob => {
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'my_resume.pdf';
            link.click();
        })
        .catch(error => {
            Swal.fire('Error', error.message, 'error');
        });
}

function customizeResume() {
    Swal.fire({
        title: 'Coming Soon!',
        text: 'Theme and section customization will be added shortly!',
        icon: 'info',
        confirmButtonColor: '#0077cc'
    });
}

function changeTemplate() {
    Swal.fire({
        title: 'Change Template?',
        text: 'You will return to the template selection screen.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#0077cc',
        cancelButtonColor: '#999',
        confirmButtonText: 'Yes, change it'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/resume/templates';
        }
    });
}
