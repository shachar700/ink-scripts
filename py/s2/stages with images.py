import pygame

pygame.init()
width=1800;
height=672
screen = pygame.display.set_mode( (width, height ) )
pygame.display.set_caption('clicked on image')
stage1 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_The_Reef_resized.png").convert()
stage2 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Musselforge_Fitness_resized.png").convert()
stage3 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Starfish_Mainstage_resized.png").convert()
stage4 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Humpback_Pump_Track_resized.png").convert()
stage5 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Inkblot_Art_Academy_resized.png").convert()
stage6 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Sturgeon_Shipyard_resized.png").convert()
stage7 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Moray_Towers_resized.png").convert()
stage8 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Port_Mackerel_resized.png").convert()
stage9 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Manta_Maria_resized.png").convert()
stage10 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Kelp_Dome_resized.png").convert()
stage11 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Snapper_Canal_resized.png").convert()
stage12 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Blackbelly_Skatepark_resized.png").convert()
stage13 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_MakoMart_resized.png").convert()
stage14 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Walleye_Warehouse_resized.png").convert()
stage15 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Shellendorf_Institute_resized.png").convert()
stage16 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Arowana_Mall_resized.png").convert()
stage17 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Goby_Arena_resized.png").convert()
stage18 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Piranha_Pit_resized.png").convert()
stage19 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Camp_Triggerfish_resized.png").convert()
stage20 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Wahoo_World_resized.png").convert()
stage21 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_New_Albacore_Hotel_resized.png").convert()
stage22 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Ancho-V_Games_resized.png").convert()
stage23 = pygame.image.load("C:\\Users\\User\\Documents\\python scripts\\stages\\S2_Stage_Skipper_Pavilion_resized.png").convert()

screen.blit(stage1 ,  ( 0,0)) # paint to screen
screen.blit(stage2 ,  ( 300,0)) # paint to screen
screen.blit(stage3 ,  ( 600,0)) # paint to screen
screen.blit(stage4 ,  ( 900,0)) # paint to screen
screen.blit(stage5 ,  ( 1200,0)) # paint to screen
screen.blit(stage6 ,  ( 1500,0)) # paint to screen

screen.blit(stage7 ,  ( 0,168)) # paint to screen
screen.blit(stage8 ,  ( 300,168)) # paint to screen
screen.blit(stage9 ,  ( 600,168)) # paint to screen
screen.blit(stage10 ,  ( 900,168)) # paint to screen
screen.blit(stage11 ,  ( 1200,168)) # paint to screen
screen.blit(stage12 ,  ( 1500,168)) # paint to screen

screen.blit(stage13 ,  ( 0,336)) # paint to screen
screen.blit(stage14 ,  ( 300,336)) # paint to screen
screen.blit(stage15 ,  ( 600,336)) # paint to screen
screen.blit(stage16 ,  ( 900,336)) # paint to screen
screen.blit(stage17 ,  ( 1200,336)) # paint to screen
screen.blit(stage18 ,  ( 1500,336)) # paint to screen

screen.blit(stage19 ,  ( 0,504)) # paint to screen
screen.blit(stage20 ,  ( 300,504)) # paint to screen
screen.blit(stage21 ,  ( 600,504)) # paint to screen
screen.blit(stage22 ,  ( 900,504)) # paint to screen
screen.blit(stage23 ,  ( 1200,504)) # paint to screen

pygame.display.flip() # paint screen one time

f = open("C:\\Users\\User\\Documents\\python scripts\\stages\\stages_w_images.txt", "a")
f.write("== Stages ==" + '\n')
f.write("{| align=\"left\" cellpadding=\"1px\" style=\"background:#FFFFFF; text-align:center; border: 3px solid #F03C78; {{roundy}}" + '\n')
f.write("|-" + '\n')
f.write("! colspan=\"4\"|Stages in [[File:Mode_Icon_Splat_Zones.png|24px]] [[Splat Zones]]" + '\n')
f.write("|-" + '\n')

stage = []

i=0
running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            x, y = event.pos

            stage1_rect = stage1.get_rect(topleft = (0, 0))
            if stage1_rect.collidepoint(x,y):
                stage.append("The Reef")
                
            stage2_rect = stage2.get_rect(topleft = (300, 0))
            if stage2_rect.collidepoint(x,y):
                stage.append("Musselforge Fitness")
                
            stage3_rect = stage3.get_rect(topleft = (600, 0))
            if stage3_rect.collidepoint(x,y):
                stage.append("Starfish Mainstage")
                
            stage4_rect = stage4.get_rect(topleft = (900, 0))
            if stage4_rect.collidepoint(x,y):
                stage.append("Humpback Pump Track")
                            
            stage5_rect = stage5.get_rect(topleft = (1200, 0))
            if stage5_rect.collidepoint(x,y):
                stage.append("Inkblot Art Academy")
                
            stage6_rect = stage6.get_rect(topleft = (1500, 0))
            if stage6_rect.collidepoint(x,y):
                stage.append("Sturgeon Shipyard")
                          
            stage7_rect = stage7.get_rect(topleft = (0, 168))
            if stage7_rect.collidepoint(x,y):
                stage.append("Moray Towers")
                
            stage8_rect = stage8.get_rect(topleft = (300, 168))
            if stage8_rect.collidepoint(x,y):
                stage.append("Port Mackerel")
                          
            stage9_rect = stage9.get_rect(topleft = (600, 168))
            if stage9_rect.collidepoint(x,y):
                stage.append("Manta Maria")             

            stage10_rect = stage10.get_rect(topleft = (900, 168))
            if stage10_rect.collidepoint(x,y):
                stage.append("Kelp Dome")
                
            stage11_rect = stage11.get_rect(topleft = (1200, 168))
            if stage11_rect.collidepoint(x,y):
                stage.append("Snapper Canal")
                
            stage12_rect = stage12.get_rect(topleft = (1500, 168))
            if stage12_rect.collidepoint(x,y):
                stage.append("Blackbelly Skatepark")
                
            stage13_rect = stage13.get_rect(topleft = (0, 336))
            if stage13_rect.collidepoint(x,y):
                stage.append("MakoMart")
                
            stage14_rect = stage14.get_rect(topleft = (300, 336))
            if stage14_rect.collidepoint(x,y):
                stage.append("Walleye Warehouse")  

            stage15_rect = stage15.get_rect(topleft = (600, 336))
            if stage15_rect.collidepoint(x,y):
                stage.append("Shellendorf Institute")
                
            stage16_rect = stage16.get_rect(topleft = (900, 336))
            if stage16_rect.collidepoint(x,y):
                stage.append("Arowana Mall")
                
            stage17_rect = stage17.get_rect(topleft = (1200, 336))
            if stage17_rect.collidepoint(x,y):
                stage.append("Goby Arena")
                
            stage18_rect = stage18.get_rect(topleft = (1500, 336))
            if stage18_rect.collidepoint(x,y):
                stage.append("Piranha Pit")
                
            stage19_rect = stage19.get_rect(topleft = (0, 504))
            if stage19_rect.collidepoint(x,y):
                stage.append("Camp Triggerfish")
                
            stage20_rect = stage20.get_rect(topleft = (300, 504))
            if stage20_rect.collidepoint(x,y):
                stage.append("Wahoo World")             

            stage21_rect = stage21.get_rect(topleft = (600, 504))
            if stage21_rect.collidepoint(x,y):
                stage.append("New Albacore Hotel")
                
            stage22_rect = stage22.get_rect(topleft = (900, 504))
            if stage22_rect.collidepoint(x,y):
                stage.append("Ancho-V Games")
                
            stage23_rect = stage23.get_rect(topleft = (1200, 504))
            if stage23_rect.collidepoint(x,y):
                stage.append("Skipper Pavilion")
            
            if len(stage) == 32:
                running = False

f.write("| [[File:S2 Stage " + stage[0] + ".png|150px|link="+stage[0]+"]]<br />[["+stage[0]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[1] + ".png|150px|link="+stage[1]+"]]<br />[["+stage[1]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[2] + ".png|150px|link="+stage[2]+"]]<br />[["+stage[2]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[3] + ".png|150px|link="+stage[3]+"]]<br />[["+stage[3]+"]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[4] + ".png|150px|link="+stage[4]+"]]<br />[["+stage[4]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[5] + ".png|150px|link="+stage[5]+"]]<br />[["+stage[5]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[6] + ".png|150px|link="+stage[6]+"]]<br />[["+stage[6]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[7] + ".png|150px|link="+stage[7]+"]]<br />[["+stage[7]+"]]" + '\n')
f.write("|" + '\n')
f.write("|}" + '\n')
f.write("" + '\n')
f.write("{| align=\"left\" cellpadding=\"1px\" style=\"background:#FFFFFF; text-align:center; border: 3px solid #F03C78; {{roundy}}" + '\n')
f.write("|-" + '\n')
f.write("! colspan=\"4\"|Stages in [[File:Mode_Icon_Tower_Control.png|24px]] [[Tower Control]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[8] + ".png|150px|link="+stage[8]+"]]<br />[["+stage[8]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[9] + ".png|150px|link="+stage[9]+"]]<br />[["+stage[9]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[10] + ".png|150px|link="+stage[10]+"]]<br />[["+stage[10]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[11] + ".png|150px|link="+stage[11]+"]]<br />[["+stage[11]+"]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[12] + ".png|150px|link="+stage[12]+"]]<br />[["+stage[12]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[13] + ".png|150px|link="+stage[13]+"]]<br />[["+stage[13]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[14] + ".png|150px|link="+stage[14]+"]]<br />[["+stage[14]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[15] + ".png|150px|link="+stage[15]+"]]<br />[["+stage[15]+"]]" + '\n')
f.write("|" + '\n')
f.write("|}" + '\n')
f.write("" + '\n')
f.write("{| align=\"left\" cellpadding=\"1px\" style=\"background:#FFFFFF; text-align:center; border: 3px solid #F03C78; {{roundy}}" + '\n')
f.write("|-" + '\n')
f.write("! colspan=\"4\"|Stages in [[File:Mode_Icon_Rainmaker.png|24px]] [[Rainmaker]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[16] + ".png|150px|link="+stage[16]+"]]<br />[["+stage[16]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[17] + ".png|150px|link="+stage[17]+"]]<br />[["+stage[17]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[18] + ".png|150px|link="+stage[18]+"]]<br />[["+stage[18]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[19] + ".png|150px|link="+stage[19]+"]]<br />[["+stage[19]+"]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[20] + ".png|150px|link="+stage[20]+"]]<br />[["+stage[20]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[21] + ".png|150px|link="+stage[21]+"]]<br />[["+stage[21]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[22] + ".png|150px|link="+stage[22]+"]]<br />[["+stage[22]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[23] + ".png|150px|link="+stage[23]+"]]<br />[["+stage[23]+"]]" + '\n')
f.write("|" + '\n')
f.write("|}" + '\n')
f.write("" + '\n')
f.write("{| align=\"left\" cellpadding=\"1px\" style=\"background:#FFFFFF; text-align:center; border: 3px solid #F03C78; {{roundy}}" + '\n')
f.write("|-" + '\n')
f.write("! colspan=\"4\"|Stages in [[File:Mode_Icon_Clam_Blitz.png|24px]] [[Clam Blitz]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[24] + ".png|150px|link="+stage[24]+"]]<br />[["+stage[24]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[25] + ".png|150px|link="+stage[25]+"]]<br />[["+stage[25]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[26] + ".png|150px|link="+stage[26]+"]]<br />[["+stage[26]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[27] + ".png|150px|link="+stage[27]+"]]<br />[["+stage[27]+"]]" + '\n')
f.write("|-" + '\n')
f.write("| [[File:S2 Stage " + stage[28] + ".png|150px|link="+stage[28]+"]]<br />[["+stage[28]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[29] + ".png|150px|link="+stage[29]+"]]<br />[["+stage[29]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[30] + ".png|150px|link="+stage[30]+"]]<br />[["+stage[30]+"]]" + '\n')
f.write("| [[File:S2 Stage " + stage[31] + ".png|150px|link="+stage[31]+"]]<br />[["+stage[31]+"]]" + '\n')
f.write("|" + '\n')
f.write("|}" + '\n')
f.write("{{-}}" + '\n')

f.close()               
pygame.quit()