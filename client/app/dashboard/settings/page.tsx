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

import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
  } from "@/components/ui/carousel"

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
  
 
const formSchema = z.object({
  username: z.string().max(30, {
    message: "Username can't be more than 30 characters.",
  }).optional(),
  email: z.string().email({
    message: "Invalid email address.",
  }).optional(),
  password: z.string().min(6, {
    message: "Password must be at least 6 characters.",
  }).optional(),
  height: z.string().transform((val) => parseInt(val, 10)).refine((val) => !isNaN(val) && (val > 0), {
    message: "Height must be a positive number.",
  }).optional(),
  weight: z.string().transform((val) => parseInt(val, 10)).refine((val) => !isNaN(val) && (val > 0), {
    message: "Weight must be a positive number.",
  }).optional(),
  age: z.string().transform((val) => parseInt(val, 10)).refine((val) => !isNaN(val) && (val > 0), {
    message: "Age must be a positive number.",
  }).optional(),
  activity_level: z.string().transform((val) => parseInt(val, 10)).refine((val) => !isNaN(val) && (val > 0), {
    message: "Activity level must be a positive number.",
  }).optional(),
  gender: z.string().transform((val) => parseInt(val, 10)).refine((val) => !isNaN(val) && (val >= 0), {
    message: "Select an option.",
  }).optional(),
  fitness_goal: z.string().transform((val) => parseInt(val, 10)).refine((val) => !isNaN(val) && (val >= 0), {
    message: "Select an option.",
  }).optional(),
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
        // defaultValues: {
        // username: "",
        // },
    })
    
    // 2. Define a submit handler.
    async function onSubmit(values: z.infer<typeof formSchema>) {
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        // console.log(values);

        // Create a new object with the transformed gender value
        const transformedValues = {
            ...values,
            gender: values.gender ? values.gender === 1 : undefined,
        };

        const definedValues = Object.fromEntries(
            Object.entries(values).filter(([_, value]) => value !== undefined)
        );

        

        // Upload the defined values to Supabase
        const { data: user } = await supabase.auth.getUser();
        const { data, error } = await supabase
            .from('Users')
            .update(definedValues)
            .eq('user_uid', user?.user?.id)
            .select();

        if (error) {
            console.error('Error uploading data:', error);
        } else {
            console.log('Data uploaded successfully:', data);
        }
    }

    return (
        <div className="flex flex-col items-center">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col">
                    <Carousel 
                        className="w-full max-w-xs"
                        opts={{
                            align: "start",
                            loop: true,
                        }}
                    >
                        <CarouselContent>
                            <CarouselItem key={1}>
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
                            </CarouselItem>
                            <CarouselItem key={2}>
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
                            </CarouselItem>
                            <CarouselItem key={3}>
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
                                    <Select onValueChange={field.onChange}>
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select the gender you identify as." />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            <SelectItem value="0">male</SelectItem>
                                            <SelectItem value="1">female</SelectItem>
                                            <SelectItem value="2">other</SelectItem>
                                            <SelectItem value="3">prefer not to specify</SelectItem>
                                        </SelectContent>
                                    </Select>
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
                                    <Select onValueChange={field.onChange}>
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select a weight goal" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            <SelectItem value="0">bulk</SelectItem>
                                            <SelectItem value="1">maintain</SelectItem>
                                            <SelectItem value="2">cut</SelectItem>
                                        </SelectContent>
                                    </Select>
                                    <FormDescription>
                                        This is your weight goal.
                                    </FormDescription>
                                    <FormMessage />
                                    </FormItem>
                                    
                                )}
                                />
                            </CarouselItem>
                        </CarouselContent>
                        <CarouselPrevious />
                        <CarouselNext />
                    </Carousel>
                    <Button type="submit">Save</Button>
                </form>
            </Form>
            <div className="pt-4"><Button onClick={handleLogout}>Log Out</Button></div>
        </div>
    );
};

export default SettingsPage;