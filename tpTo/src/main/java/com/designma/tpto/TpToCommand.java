package com.designma.tpto;

import net.minecraft.command.CommandBase;
import net.minecraft.command.CommandException;
import net.minecraft.command.ICommandSender;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.TextComponentString;

import javax.annotation.Nullable;
import java.util.Collections;
import java.util.List;

public class TpToCommand extends CommandBase {
    @Override
    public String getName() {
        return "tpto";
    }

    @Override
    public String getUsage(ICommandSender sender) {
        return "/tpto <player> - Teleport to another player at the cost of 5 XP levels.";
    }

    @Override
    public void execute(MinecraftServer server, ICommandSender sender, String[] args) throws CommandException {
        if (sender instanceof EntityPlayer) {
            EntityPlayer player = (EntityPlayer) sender;
            if (args.length == 1) {
                EntityPlayer target = server.getPlayerList().getPlayerByUsername(args[0]);
                if (target != null) {
                    double distanceToPlayer = (double) Math.sqrt(
                            Math.pow(target.posX - player.posX, 2) +
                                    Math.pow(target.posY - player.posY, 2) +
                                    Math.pow(target.posZ - player.posZ, 2));
                    double xpRequired = (distanceToPlayer / TpToConfig.maxDistance) * TpToConfig.xpCost;

                    if (player.experienceLevel >= xpRequired) {
                        player.addExperienceLevel(-(int) Math.rint(xpRequired)); // Deduct xp cost
                        player.setPositionAndUpdate(target.posX, target.posY, target.posZ);
                        player.sendMessage(
                                new TextComponentString(
                                        "Teleported to " + target.getName() + " for " + xpRequired + " XP levels!"));
                    } else {
                        player.sendMessage(
                                new TextComponentString("You need at least " + xpRequired + " XP levels to teleport!"));
                    }
                } else {
                    player.sendMessage(new TextComponentString("Player not found!"));
                }
            } else {
                player.sendMessage(new TextComponentString("Usage: /tpto <player>"));
            }
        } else {
            sender.sendMessage(new TextComponentString("This command can only be used by players!"));
        }
    }

    @Override
    public boolean checkPermission(MinecraftServer server, ICommandSender sender) {
        return true; // Allow non-admin players to use the command
    }

    // retorna una lista de jugadores online para completar con tab el primer
    // argumento
    @Override
    public List<String> getTabCompletions(MinecraftServer server, ICommandSender sender, String[] args,
            @Nullable BlockPos targetPos) {
        return args.length == 1 ? getListOfStringsMatchingLastWord(args, server.getOnlinePlayerNames())
                : Collections.emptyList();
    }
}