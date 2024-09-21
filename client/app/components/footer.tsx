import React from 'react';
import Link from "next/link";
import { useRouter } from 'next/router';
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle,
  } from "@/components/ui/navigation-menu"

const Footer: React.FC = () => {
    return (
        <footer>
            <NavigationMenu>
                <NavigationMenuList>
                    <NavigationMenuItem>
                    <Link href="/home" legacyBehavior passHref>
                        <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                        Home
                        </NavigationMenuLink>
                    </Link>
                    </NavigationMenuItem>
                </NavigationMenuList>
                <NavigationMenuList>
                    <NavigationMenuItem>
                    <Link href="/settings" legacyBehavior passHref>
                        <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                        Settings
                        </NavigationMenuLink>
                    </Link>
                    </NavigationMenuItem>
                </NavigationMenuList>
                <NavigationMenuList>
                    <NavigationMenuItem>
                    <Link href="/profile" legacyBehavior passHref>
                        <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                        Profile
                        </NavigationMenuLink>
                    </Link>
                    </NavigationMenuItem>
                </NavigationMenuList>
            </NavigationMenu>
        </footer>
    );
};

export default Footer;