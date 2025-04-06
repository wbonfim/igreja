from django.core.management.base import BaseCommand
from apps.igrejas.models import TemplateIgreja

class Command(BaseCommand):
    help = 'Cria templates padrão para as igrejas'

    def handle(self, *args, **kwargs):
        template_moderno = {
            'nome': 'Impacto Visual',
            'html': '''
                <section id="cultos" class="section">
                    <div class="container">
                        <h2>Horários dos Cultos</h2>
                        <div class="horarios">
                            {% for linha in igreja.horario_cultos.splitlines %}
                                <div class="horario-item">{{ linha }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </section>

                <section id="endereco" class="section">
                    <div class="container">
                        <h2>Localização</h2>
                        <div class="endereco-info">
                            <p><i class="fas fa-map-marker-alt"></i> {{ igreja.endereco }}</p>
                            <p>{{ igreja.bairro }} - {{ igreja.cidade }}/{{ igreja.estado }}</p>
                            <p>CEP: {{ igreja.cep }}</p>
                        </div>
                    </div>
                </section>

                <section id="contato" class="section">
                    <div class="container">
                        <h2>Entre em Contato</h2>
                        <div class="contato-info">
                            <p><i class="fas fa-phone"></i> {{ igreja.telefone }}</p>
                            <p><i class="fas fa-envelope"></i> {{ igreja.email }}</p>
                        </div>
                    </div>
                </section>
            ''',
            'css': '''
                .section {
                    padding: 5rem 2rem;
                    background: #fff;
                }

                .section:nth-child(even) {
                    background: #f8f9fa;
                }

                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }

                h2 {
                    text-align: center;
                    color: var(--primary-color);
                    margin-bottom: 2rem;
                    font-size: 2.5rem;
                }

                .horarios {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                    max-width: 600px;
                    margin: 0 auto;
                }

                .horario-item {
                    background: #fff;
                    padding: 1rem;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    text-align: center;
                    font-size: 1.2rem;
                }

                .endereco-info, .contato-info {
                    text-align: center;
                    font-size: 1.2rem;
                }

                .endereco-info p, .contato-info p {
                    margin: 0.5rem 0;
                }

                .fas {
                    color: var(--primary-color);
                    margin-right: 0.5rem;
                }

                @media (max-width: 768px) {
                    .section {
                        padding: 3rem 1rem;
                    }

                    h2 {
                        font-size: 2rem;
                    }

                    .horario-item {
                        font-size: 1rem;
                    }
                }
            ''',
            'js': '''
                document.addEventListener('DOMContentLoaded', function() {
                    // Adiciona classe active ao link do menu atual
                    const sections = document.querySelectorAll('.section');
                    const navLinks = document.querySelectorAll('.nav-link');

                    window.addEventListener('scroll', () => {
                        let current = '';
                        sections.forEach(section => {
                            const sectionTop = section.offsetTop;
                            const sectionHeight = section.clientHeight;
                            if (scrollY >= (sectionTop - sectionHeight / 3)) {
                                current = section.getAttribute('id');
                            }
                        });

                        navLinks.forEach(link => {
                            link.classList.remove('active');
                            if (link.getAttribute('href').slice(1) === current) {
                                link.classList.add('active');
                            }
                        });
                    });

                    // Scroll suave para links internos
                    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                        anchor.addEventListener('click', function (e) {
                            e.preventDefault();
                            document.querySelector(this.getAttribute('href')).scrollIntoView({
                                behavior: 'smooth'
                            });
                        });
                    });
                });
            '''
        }

        TemplateIgreja.objects.get_or_create(
            nome=template_moderno['nome'],
            defaults={
                'html': template_moderno['html'],
                'css': template_moderno['css'],
                'js': template_moderno['js']
            }
        )

        self.stdout.write(
            self.style.SUCCESS('Templates padrão criados com sucesso!')
        )
