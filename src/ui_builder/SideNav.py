import os
from html5print import HTMLBeautifier

class SideNav():

    def __init__(self, side_navs):
        self.side_navs = side_navs

    def build_page(self, path):
        side_nav_list = ""
        for link, icon, name in self.side_navs:
            side_nav_list += f"""
            <mat-list-item [routerLink]="['{link}']" routerLinkActive="active" (click)="toggleSidenav()">
              <mat-icon mat-list-icon>{icon}</mat-icon>
              <p matLine>{name}</p>
            </mat-list-item>
            """
        html = f"""
        <mat-drawer-container class="container--main">
          <mat-drawer class="container--main__drawer"
                      #sideNav
                      [mode]="mode"
                      [style.width]="sideNavWidth">
            <mat-nav-list>
              {side_nav_list}
            </mat-nav-list>
          </mat-drawer>

          <mat-drawer-content>
            <ng-content>
            </ng-content>

            <footer>
              <div class="powered-by">
                Powered by <img class="logo" src="../assets/images/oncorps-grey.svg" alt="OnCorps">
              </div>
            </footer>
          </mat-drawer-content>
        </mat-drawer-container>
        """

        with open(f"{path}/side-nav.component.html", 'w') as html_file:
            # html_file.write(HTMLBeautifier.beautify(html))
            html_file.write(html)
