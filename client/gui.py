import queue

import pygame
import pygame_gui


def gui(stateQueue, eventQueue, logQueue):
    pygame.init()

    # create a screen of width=800, height=600
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)

    # Create the GUI manager
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Connection url
    urlBox = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((175, 150), (575, 50)), initial_text='raspberrypi.local:65432', manager=manager)

    # Connect button
    connectButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (50, 150), (125, 50)), text='Connect', manager=manager)
    is_connected = False

    # Log area
    logBox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(
        (50, 200), (700, 300)), html_text='', manager=manager)

    # Exit button
    exitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (625, 500), (125, 50)), text='Exit', manager=manager)

    # Keys display box
    displayBox = pygame.Rect((WIDTH - 400) / 2, 75, 400, 50)

    pygame.display.set_caption('Kbdrelay')
    pygame.display.set_icon(pygame.image.load('assets/Kbdrelay.png'))

    running = True
    clock = pygame.time.Clock()

    keys_down = []

    # Output the log in textbox
    def log(logArea, logHtml):
        logArea.append_html_text(logHtml)
        logArea.rebuild()
        if logArea.scroll_bar:
            logArea.scroll_bar.set_scroll_from_start_percentage(1.0)

    while running:
        time_delta = clock.tick(60)/1000.0
        screen.fill((0, 0, 0))

        # Receive connection state
        try:
            is_connected = stateQueue.get(0)
            if is_connected:
                connectButton.set_text('Disconnect')
            else:
                connectButton.set_text('Connect')
            connectButton.enable()
        except queue.Empty:
            pass

        # Receive logs
        try:
            logString = logQueue.get(0)
            log(logBox, logString)
        except queue.Empty:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                keys_down.append(pygame.key.name(event.key))

            elif event.type == pygame.KEYUP:
                keys_down.remove(pygame.key.name(event.key))

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == connectButton:
                    connectButton.disable()
                    if not is_connected:
                        print(urlBox.get_text())
                        eventQueue.put(
                            {'cmd': 'connect', 'data': urlBox.get_text()})
                    else:
                        eventQueue.put({'cmd': 'disconnect', 'data': ''})

                if event.ui_element == exitButton:
                    running = False

            manager.process_events(event)

        # Keys display box
        pygame.draw.rect(screen, pygame.Color('#1a2332'), displayBox)
        pygame.draw.rect(screen, (255, 255, 255), displayBox, 2)
        displayBoxLabel = font.render(
            f'Keys down', True, pygame.Color('#a4b1cd'))

        # Write active keys
        activeKeys = font.render(
            f'{keys_down}', True, pygame.Color('#9fef00'))

        # Active keys frame
        screen.blit(displayBoxLabel,
                    ((WIDTH - displayBoxLabel.get_size()[0])/2, 50))
        screen.blit(activeKeys, ((WIDTH - activeKeys.get_size()
                    [0])/2, displayBox.top + (displayBox.height - activeKeys.get_size()[1]) / 2))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
