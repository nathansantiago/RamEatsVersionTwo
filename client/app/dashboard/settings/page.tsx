"use client"
 
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { supabase } from '../../../lib/supabase';
import { useRouter } from 'next/navigation';
import { z } from "zod"
 
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
 
const formSchema = z.object({
  username: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
  email: z.string().email({
    message: "Invalid email address.",
  }),
  password: z.string().min(6, {
    message: "Password must be at least 6 characters.",
  }),
  height: z.string().min(1, {
    message: "Height is required.",
  }),
  weight: z.string().min(1, {
    message: "Weight is required.",
  }),
  age: z.string().min(1, {
    message: "Age is required.",
  }),
  activity_level: z.string().min(1, {
    message: "Activity level is required.",
  }),
  gender: z.string().min(1, {
    message: "Gender is required.",
  }),
  fitness_goal: z.string().min(1, {
    message: "Fitness goal is required.",
  }),
})

const SettingsPage: React.FC = () => {
    const router = useRouter();

    const handleLogout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) console.error('Error logging out:', error.message);
        else {
            console.log('User logged out');
            router.replace('/');
        }
    };

    // 1. Define your form.
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
        username: "",
        },
    })
    
    // 2. Define a submit handler.
    function onSubmit(values: z.infer<typeof formSchema>) {
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        console.log(values)
    }

    return (
        <div className="flex flex-col items-center">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="grid grid-cols-3 gap-3">
                    <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Username</FormLabel>
                        <FormControl>
                            <Input placeholder="shadcn" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your public display name.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                            <Input placeholder="email@email.com" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your email.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Password</FormLabel>
                        <FormControl>
                            <Input placeholder="password" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your password.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="height"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Height</FormLabel>
                        <FormControl>
                            <Input placeholder="56" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your height in inches.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="weight"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Weight</FormLabel>
                        <FormControl>
                            <Input placeholder="120" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your weight in pounds.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="age"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Age</FormLabel>
                        <FormControl>
                            <Input placeholder="20" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your age in years.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="activity_level"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Activity Level</FormLabel>
                        <FormControl>
                            <Input placeholder="2200" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your estimated calories burned per day.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="gender"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Gender</FormLabel>
                        <FormControl>
                            <Input placeholder="female" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is the gender you identify as.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="fitness_goal"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Fitness Goal</FormLabel>
                        <FormControl>
                            <Input placeholder="maintain" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your weight goals.
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                        
                    )}
                    />
                    <Button type="submit">Submit</Button>
                </form>
            </Form>
            <div className="pt-4"><Button onClick={handleLogout}>Log Out</Button></div>
        </div>
    );
};

export default SettingsPage;