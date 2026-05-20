output "public_ip_address" {
  description = "VM Public IP address"
  value       = azurerm_linux_virtual_machine.vm.public_ip_address
}