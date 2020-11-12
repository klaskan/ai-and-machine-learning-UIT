'''
#
# Obligatorisk karaktersatt oppgave #1
#
# Legg spesielt merke til at det er kun koden i klassen Kalman som kan endres. Det er også koden som skal leveres inn
# Det er derfor viktig at INGEN ANNEN KODE ENDRES !!! 
#
'''
import pygame as pg
from random import random,randint
import numpy as np
from numpy.linalg import norm

fps = 0.0

class Projectile():

    def __init__(self, background, kalman=None):
        self.background = background
        self.rect = pg.Rect((800,700),(16,16))
        self.px = self.rect.x
        self.py = self.rect.y
        self.dx = 0.0
        self.kalm = kalman

    def move(self,goal):

        if self.kalm:
            goal = self.kalm.calc_next(goal)

        deltax = np.array(float(goal) - self.px)
        #print(delta2)
        mag_delta = norm(deltax)#* 500.0
        np.divide(deltax,mag_delta,deltax)

        self.dx += deltax
        #if self.dx:
            #self.dx /= norm(self.dx) * 50

        self.px += self.dx /50.0
        self.py += -0.5
        try:
            self.rect.x = int(self.px)
        except:
            pass
        try:
            self.rect.y = int(self.py)
        except:
            pass


class Target():

    def __init__(self, background, width):
        self.background = background
        self.rect = pg.Rect(self.background.get_width()//2-width//2, 
            50, width, 32)
        self.dx = 1 if random() > 0.5 else -1

    def move(self):
        self.rect.x += self.dx

        if self.rect.x < 300 or self.rect.x > self.background.get_width()-300:
            self.dx *= -1

    def noisy_x_pos(self):
        pos = self.rect.x
        center = self.rect.width//2
        noise = np.random.normal(0,1,1)[0]

        return pos + center + noise*300.0


class Kalman:
    """En Kalman implementasjon
        Her implementerer vi et endimensjonalt kalman filter som skal predikerer bevegelsene til
        en et objekt i et ferdig spill laget i pygame. Det bevegelige måle vi skal treffe ved 
        hjelp av kalman filteret er en rosa boks som beveger seg men en konstant hastighet 
        langs en x akse. Den rosa boksen starter midt i spill vinduet og beveger seg mot venster
        eller høyre i en konstant hastighet, til den treffer en enden og beveger seg tilbake. 
        
        Thought process:
            Jeg startet først med å definere det underliggende problemet, og bevegelsesmodellen som er 
            en matematisk model av det underliggende systemer som ser slik ut: x_{t+1} = x_t + dt*v 
            Denne modellen beskriver hvordan det underliggende systemet beveger seg. Derretter så jeg på
            den dataen jeg fikk inn fra simulasjonen i pygame. calc_next() metoden tok inn 46 datapunk i 
            sekundet, hvor alle data hadde en god del støy. Kalman modellen krever også at man definerer 
            usikkerheten i den dynamisk modellen og målingsusikkerheten. Siden vi har fått oppgitt at det
            er en relativ høy varians i målingene må vi sette måleusikkerheten til en relativ høy verdi.
            Når det kommer til usikkerheten til den dynamsike modellen, kan vi med ganske høy sikkerhet si
            at denne ligningen beskriver bevegelsene til systemet vårt, derfor setter vi denne veldig lavt.
            Kalman gain blir også beregnet ut fra usikkerheten knyttet til den predikerte posisjonen og 
            måleusikkerheten, det blir et slags vektet gjennomsnitt av systemets predikerte state og den 
            observerte staten. Dersom kalman filteret har en høy verdi (nært 1), betyr det at man har mindre
            usikkerhet knyttet til målene. Så når man har et kalman gain som er nært 1 betyr dette at man 
            vektlegger målingene mer en de predikerte verdiene som kommer fra den matematiske modellen vår.
            Dersom kalman gainet skulle vært velig lavt, nært 0 betyr dette at man skal legge mer vekt på 
            modellens prediksjoner enn målene. Så man ser med andre ord på hvilken av de to metodene som
            har mest usikkerhet knyttet til seg, og vektlegger den med minst usikkerhet. En stor ting i 
            Kalman filteret og maskinlæring generelt er tuning av modellen, og dette har jeg også i stor
            grad prøvd å gjøre. Nedenfor har jeg satt opp alle argumentene som inngår og hvorfor jeg har 
            valgt den verdien jeg har.
            
            
        
        Args:
            x (numpy.float64): Blir orginalt satt til float verdien 800. Fordi vi starter ut på midten av
                                av vinduet. Men denne verdien blir forandret satt til zi. 
            
            p (float): dette er usikkerheten knyttet til den predikerte posisjonen. Denne har jeg valgt å
                        sette til 5.0 siden den matematiske modellen forklarer veldig bra hvor firkanten
                        egentlig skulle vært. Her er det målestøyen som gir usikkerhet. 
            
            
            dt (float): Dette er tids intervalle for oppdatering. Siden modellen er satt til 300 frames 
                        per sekun (fps), betyr dette at bildet blir refresher(tegnet på nytt) 300 ganger 
                        i sekundet. Men det betyr ikke at boksen beveger seg 300px i sekundet. Så derfor
                        har jeg har valgt og sette dt = 1, etter en del tuning. 
            
            v (float): Dette er velocity av det firkantede objektet. Denne har jeg valgt å sette til 
                        3 som et resultat av mye tuning. 
            
            p_v (float): Dette er usikkerheten knyttet til velocity av det firkentede objektet. Altså 
                        er det usikkerheten knyttet til (v) argumentet. Satt til å være lik null som 
                        resultat av mye tuning. 
                        
            
            q (float): Er usikkerheten knyttet til systemets dynamiske model. Med andre ord er det usikkerheten
                        knyttet til fysikk modellen knyttet til bevegelse langs en akse med konstant fart. 
                        Denne har jeg satt lav siden jeg har tro på at den underliggende dynamiske modellens 
                        forklaringskraft.
                        
            r (float): Er måleusikkerheten. Vi vet at målestøyen er relativt høy. Denne har jeg satt til å være 
                        300 etter informasjonen vi fikk i oppgaven.
            
            
        Returns:
            x (float): returnerer calculerte neste posisjonen.
        
        
        
        
        
    """
    def __init__(self, x_0 = 800.0, p = 5., dt = 1., v =3. , p_v = 0., q = 1., r = 300.):

        self.x = x_0
        self.p = p
        self.dt = dt
        self.v = v 
        self.p_v = p_v 
        self.q = q
        self.r = r
    
    def calc_next(self, zi):
        #Predict
        self.x = self.x + self.dt*self.v
        self.p = self.p + ((self.dt**2) * self.p_v) + self.q
        
        #find kalman gain
        k = self.p / (self.p + self.r)
        
        #Update state and state uncertainty
        self.x = self.x + k * (zi - self.x)
        p = (1 - k) * self.p
        return self.x




if __name__ == "__main__":
    pg.init()

    w,h = 1600,800

    background = pg.display.set_mode((w,h))
    surf = pg.surfarray.pixels3d(background)
    running = True
    clock = pg.time.Clock()

    kalman_score = 0
    reg_score = 0
    iters = 0

    while running:
        target = Target(background, 32)
        missile = Projectile(background)
        k_miss = Projectile(background,Kalman()) #kommenter inn denne linjen naar Kalman er implementert
        last_x_pos = target.noisy_x_pos
        noisy_draw = np.zeros((w,20))

        trial = True
        iters += 1

        while trial:

            # Setter en maksimal framerate på 300. Hvis dere vil øke denne er dette en mulig endring
            clock.tick(300)
            
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False
            
            background.fill(0x448844)
            surf[:,0:20,0] = noisy_draw

            last_x_pos = target.noisy_x_pos()
            #print(last_x_pos)

            target.move()
            missile.move(last_x_pos)
            
            
            k_miss.move(last_x_pos) #kommenter inn denne linjen naar Kalman er implementert

            pg.draw.rect(background, (255, 200, 0), missile.rect)
            pg.draw.rect(background, (0, 200, 255), k_miss.rect) #kommenter inn denne linjen naar Kalman er implementert
            pg.draw.rect(background, (255, 200, 255), target.rect)

            noisy_draw[int(last_x_pos):int(last_x_pos)+20,:] = 255
            noisy_draw -= 1
            np.clip(noisy_draw, 0, 255, noisy_draw)

            coll = missile.rect.colliderect(target.rect)
            k_coll = k_miss.rect.colliderect(target.rect) #kommenter inn denne linjen naar Kalman er implementert#

            if coll:
                reg_score += 1

            if k_coll:    #kommenter inn denne linjen naar Kalman er implementert
                kalman_score += 1

            oob = missile.rect.y < 20

            if oob or coll or k_coll: #endre denne sjekken slik at k_coll ogsaa er med naar kalman er implementert
                trial = False

            pg.display.flip()

        print('kalman score: ', round(kalman_score/iters,2)) #kommenter inn denne linjen naar Kalman er implementert
        print('regular score: ', round(reg_score/iters,2))

    pg.quit()