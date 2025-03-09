document.addEventListener('DOMContentLoaded', function() {
    // Configurar el gráfico de precisión con animación
    if (document.getElementById('accuracyChart')) {
        const ctx = document.getElementById('accuracyChart').getContext('2d');
        
        // Crear gradiente para el gráfico
        let gradient = ctx.createLinearGradient(0, 0, 0, 200);
        gradient.addColorStop(0, '#4cc9f0');
        gradient.addColorStop(1, '#4361ee');
        
        const accuracyChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Precisión', 'Margen de error'],
                datasets: [{
                    data: [83.58, 16.42],
                    backgroundColor: [
                        gradient,
                        '#e9ecef'
                    ],
                    borderWidth: 0,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                family: 'Poppins',
                                size: 12
                            },
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.raw + '%';
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        padding: 10,
                        cornerRadius: 10,
                        boxPadding: 5
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            }
        });
    }
    
    // Calculadora de IMC mejorada
    const calculateBmiBtn = document.getElementById('calculateBmi');
    if (calculateBmiBtn) {
        calculateBmiBtn.addEventListener('click', function() {
            const height = parseFloat(document.getElementById('height').value);
            const weight = parseFloat(document.getElementById('weight').value);
            
            if (isNaN(height) || isNaN(weight) || height <= 0 || weight <= 0) {
                alert('Por favor, ingresa valores válidos para altura y peso.');
                return;
            }
            
            // Calcular IMC: peso(kg) / (altura(m))²
            const heightInMeters = height / 100;
            const bmi = weight / (heightInMeters * heightInMeters);
            
            // Mostrar el resultado
            document.getElementById('bmiValue').textContent = bmi.toFixed(1);
            
            // Determinar categoría y color
            let category, colorClass;
            if (bmi < 18.5) {
                category = 'Bajo peso';
                colorClass = 'alert-warning';
            } else if (bmi < 25) {
                category = 'Peso normal';
                colorClass = 'alert-success';
            } else if (bmi < 30) {
                category = 'Sobrepeso';
                colorClass = 'alert-warning';
            } else {
                category = 'Obesidad';
                colorClass = 'alert-danger';
            }
            
            document.getElementById('bmiCategory').textContent = category;
            
            const bmiResult = document.getElementById('bmiResult');
            bmiResult.classList.remove('d-none', 'alert-info', 'alert-success', 'alert-warning', 'alert-danger');
            bmiResult.classList.add(colorClass);
            
            document.getElementById('useBmiValue').classList.remove('d-none');
            
            // Animación de aparición
            bmiResult.style.opacity = '0';
            bmiResult.style.transform = 'translateY(10px)';
            
            setTimeout(() => {
                bmiResult.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                bmiResult.style.opacity = '1';
                bmiResult.style.transform = 'translateY(0)';
            }, 100);
        });
    }
    
    // Usar el valor de IMC calculado en el formulario principal
    const useBmiValueBtn = document.getElementById('useBmiValue');
    if (useBmiValueBtn) {
        useBmiValueBtn.addEventListener('click', function() {
            const bmiValue = document.getElementById('bmiValue').textContent;
            document.getElementById('bmi').value = bmiValue;
            
            // Cerrar el modal
            const bmiModal = bootstrap.Modal.getInstance(document.getElementById('bmiCalculatorModal'));
            bmiModal.hide();
            
            // Efecto de resaltado en el campo IMC
            const bmiField = document.getElementById('bmi');
            bmiField.style.backgroundColor = '#ebfbee';
            bmiField.style.transition = 'background-color 1s ease';
            
            setTimeout(() => {
                bmiField.style.backgroundColor = '';
            }, 1500);
        });
    }
    
    // Validación de formulario mejorada
    const form = document.getElementById('diabetesForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const errorMessages = [];
            
            // Validar IMC
            const bmi = parseFloat(document.getElementById('bmi').value);
            if (isNaN(bmi) || bmi < 10 || bmi > 100) {
                isValid = false;
                errorMessages.push('Por favor, ingresa un IMC válido entre 10 y 100.');
                document.getElementById('bmi').classList.add('is-invalid');
            } else {
                document.getElementById('bmi').classList.remove('is-invalid');
            }
            
            // Validar condiciones preexistentes
            const preExistingConditions = document.getElementById('pre_existing_conditions').value;
            if (!preExistingConditions) {
                isValid = false;
                errorMessages.push('Por favor, selecciona el número de condiciones preexistentes.');
                document.getElementById('pre_existing_conditions').classList.add('is-invalid');
            } else {
                document.getElementById('pre_existing_conditions').classList.remove('is-invalid');
            }
            
            // Validar salud general
            const genHlth = document.getElementById('gen_hlth').value;
            if (!genHlth) {
                isValid = false;
                errorMessages.push('Por favor, selecciona tu nivel de salud general.');
                document.getElementById('gen_hlth').classList.add('is-invalid');
            } else {
                document.getElementById('gen_hlth').classList.remove('is-invalid');
            }
            
            // Validar grupo de edad
            const age = document.getElementById('age').value;
            if (!age) {
                isValid = false;
                errorMessages.push('Por favor, selecciona tu grupo de edad.');
                document.getElementById('age').classList.add('is-invalid');
            } else {
                document.getElementById('age').classList.remove('is-invalid');
            }
            
            // Validar dificultad para caminar
            const diffWalkOptions = document.querySelectorAll('input[name="diff_walk"]:checked');
            if (diffWalkOptions.length === 0) {
                isValid = false;
                errorMessages.push('Por favor, indica si tienes dificultad para caminar.');
                document.getElementById('diff_walk_no').classList.add('is-invalid');
                document.getElementById('diff_walk_yes').classList.add('is-invalid');
            } else {
                document.getElementById('diff_walk_no').classList.remove('is-invalid');
                document.getElementById('diff_walk_yes').classList.remove('is-invalid');
            }
            
            if (!isValid) {
                event.preventDefault();
                
                // Mostrar mensaje de error con todos los problemas
                let errorHTML = '<div class="alert alert-danger"><ul class="mb-0">';
                errorMessages.forEach(msg => {
                    errorHTML += `<li>${msg}</li>`;
                });
                errorHTML += '</ul></div>';
                
                // Insertar mensaje de error
                const errorContainer = document.createElement('div');
                errorContainer.innerHTML = errorHTML;
                
                // Eliminar mensajes de error anteriores
                const oldMessages = form.querySelectorAll('.alert-danger');
                oldMessages.forEach(msg => msg.remove());
                
                // Agregar el nuevo mensaje
                form.insertBefore(errorContainer.firstChild, form.firstChild);
                
                // Desplazarse al principio del formulario
                window.scrollTo({ top: form.offsetTop - 50, behavior: 'smooth' });
            } else {
                // Mostrar indicador de carga si el formulario es válido
                const submitBtn = form.querySelector('button[type="submit"]');
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analizando datos...';
                submitBtn.disabled = true;
                
                // Cambiar opacidad del formulario para indicar procesamiento
                form.style.opacity = '0.7';
                form.style.transition = 'opacity 0.3s ease';
            }
        });
    }
    
    // Animaciones al hacer scroll mejoradas
    function revealOnScroll() {
        const elements = document.querySelectorAll('.card, .info-card, .feature-icon');
        
        elements.forEach((element, index) => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 50) {
                setTimeout(() => {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, index * 50); // Efecto escalonado
            }
        });
    }
    
    // Inicializar elementos con opacidad 0
    document.querySelectorAll('.card, .info-card, .feature-icon').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
    });
    
    // Ejecutar la función al cargar la página y al hacer scroll
    window.addEventListener('load', revealOnScroll);
    window.addEventListener('scroll', revealOnScroll);
    
    // Tooltips para elementos informativos
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            animation: true,
            delay: { show: 100, hide: 100 }
        });
    });
    
    // Efectos hover personalizados para los iconos de características
    const featureIcons = document.querySelectorAll('.feature-icon');
    featureIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) translateY(-10px)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
});