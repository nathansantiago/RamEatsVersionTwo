"use client"

import Image from "next/image";
import RamEatsLogo from "../public/RamEatsLogo (1).png";
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { supabase } from "@/lib/supabase";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const router = useRouter();

  useEffect(() => {
    const checkSession = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (session) {
        router.push("/dashboard/home");
      }
    };
    if (typeof window !== 'undefined') {
      checkSession();
    }
  }, [router]);

  async function handleLogin() {
    // Check for null values
    if (!email || !password) {
      alert("Email and password are required.");
      return;
    }
    
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      alert(error.message);
    } else {
      const { data: { session } } = await supabase.auth.getSession();
      if (session) {
        router.push("/dashboard/home");
      }
    }
  }

  async function handleRegister() {
    // Check for null values
    if (!email || !password || !username) {
      alert("Email, password, and username are required.");
      return;
    }

    // Check for duplicate email
    const { data: emailData, error: emailError } = await supabase
      .from('Users')
      .select('email')
      .eq('email', email)
      .single();

    if (emailError && emailError.code !== 'PGRST116') {
      alert("Error checking email: " + emailError.message);
      return;
    }

    if (emailData) {
      alert("Email is already in use.");
      return;
    }

    // Check for duplicate username
    const { data: usernameData, error: usernameError } = await supabase
      .from('Users')
      .select('username')
      .eq('username', username)
      .single();

    if (usernameError && usernameError.code !== 'PGRST116') {
      alert("Error checking username: " + usernameError.message);
      return;
    }

    if (usernameData) {
      alert("Username is already in use.");
      return;
    }

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });
    
    if (error) {
      alert(error.message);
    } else {
      // Extract the uuid from the signed-up user
      const uuid = data.user?.id;
  
      if (uuid) {
        // Insert the uuid and email into the Users table
        const { error: insertError } = await supabase
          .from('Users')
          .insert([{ user_uid: uuid, email, username }]);
        if (insertError) {
          alert("Error inserting user into Users table: " + insertError.message);
        } else {
          alert("Registered " + email + " successfully!");
        }
      } else {
        alert("Error: User ID not found.");
      }
    }
  }

  return (
    <main className="min-h-screen flex justify-center items-center flex-col">
      <Image
          className="mb-8"
          src={RamEatsLogo}
          alt="RamEats logo"
          width={100}
          priority
        />
      <h1 className="mb-8 title">RamEats</h1>
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Login</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Login</DialogTitle>
            <DialogDescription>
              Enter your username and password to login to your account.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="username" className="text-right">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                className="col-span-3"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="password" className="text-right">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                value={password}
                className="col-span-3"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" onClick={handleLogin}>Login</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Register</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Register</DialogTitle>
            <DialogDescription>
              Enter your username, email, and password to register your account.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="username" className="text-right">
                Username
              </Label>
              <Input
                id="username"
                type="text"
                className="col-span-3"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="email" className="text-right">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                className="col-span-3"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="password" className="text-right">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                className="col-span-3"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" onClick={handleRegister}>Register</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </main>
  );
}
